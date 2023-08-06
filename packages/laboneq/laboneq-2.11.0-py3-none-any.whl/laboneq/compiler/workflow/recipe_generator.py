# Copyright 2022 Zurich Instruments AG
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from laboneq.compiler.code_generator.measurement_calculator import IntegrationTimes
from laboneq.compiler.common.device_type import DeviceType
from laboneq.compiler.experiment_access.experiment_dao import ExperimentDAO
from laboneq.core.types.enums.acquisition_type import AcquisitionType
from laboneq.data.compilation_job import ParameterInfo

if TYPE_CHECKING:
    from laboneq.compiler.workflow.compiler import LeaderProperties

_logger = logging.getLogger(__name__)


class RecipeGenerator:
    def __init__(self):
        self._recipe = {}
        self._recipe[
            "$schema"
        ] = "../../interface/qccs/interface/schemas/recipe-schema-1_4_0.json"
        self._recipe["line_endings"] = "unix"
        self._recipe["header"] = {
            "version": "1.4.0",
            "unit": {"time": "s", "frequency": "Hz", "phase": "rad"},
            "epsilon": {"time": 1e-12},
        }
        self._recipe["experiment"] = {"realtime_execution_init": []}

    def add_oscillator_params(self, experiment_dao: ExperimentDAO):
        oscillator_params = []
        for signal_id in experiment_dao.signals():
            signal_info = experiment_dao.signal_info(signal_id)
            oscillator_info = experiment_dao.signal_oscillator(signal_id)
            if oscillator_info is None:
                continue
            if oscillator_info.is_hardware:
                if isinstance(oscillator_info.frequency, ParameterInfo):
                    frequency, param = None, oscillator_info.frequency.uid
                else:
                    frequency, param = oscillator_info.frequency, None

                for ch in signal_info.channels:
                    oscillator_param = {
                        "id": oscillator_info.uid,
                        "device_id": signal_info.device_id,
                        "channel": ch,
                        "frequency": frequency,
                        "param": param,
                    }
                    oscillator_params.append(oscillator_param)

        self._recipe["experiment"]["oscillator_params"] = oscillator_params

    def add_integrator_allocations(
        self,
        integration_unit_allocation,
        experiment_dao: ExperimentDAO,
        integration_weights,
    ):
        def _make_integrator_allocation(signal_id: str, integrator):
            weights = {}
            if signal_id in integration_weights:
                weights = next(iter(integration_weights[signal_id].values()), {})
            integrator_allocation = {
                "signal_id": signal_id,
                "device_id": integrator["device_id"],
                "awg": integrator["awg_nr"],
                "channels": integrator["channels"],
                "weights": weights.get("basename"),
            }
            threshold = experiment_dao.threshold(signal_id)
            if threshold is not None:
                integrator_allocation["threshold"] = threshold
            return integrator_allocation

        self._recipe["experiment"]["integrator_allocations"] = [
            _make_integrator_allocation(signal_id, integrator)
            for signal_id, integrator in integration_unit_allocation.items()
        ]

    def add_acquire_lengths(self, integration_times: IntegrationTimes):
        self._recipe["experiment"]["acquire_lengths"] = [
            {
                "section_id": section_id,
                "signal_id": signal_id,
                "acquire_length": integration_info.length_in_samples,
            }
            for section_id, section_integration_time in integration_times.items()
            for signal_id, integration_info in section_integration_time.items()
            if not integration_info.is_play
        ]

    def add_devices_from_experiment(self, experiment_dao: ExperimentDAO):
        devices = []
        initializations = []
        for device in experiment_dao.device_infos():
            devices.append(
                {"device_uid": device.uid, "driver": device.device_type.upper()}
            )
            initializations.append({"device_uid": device.uid, "config": {}})
        self._recipe["devices"] = devices
        self._recipe["experiment"]["initializations"] = initializations

    def add_acquisition_type_from_experiment(self, experiment_dao: ExperimentDAO):
        self._recipe["experiment"]["acquisition_type"] = (
            AcquisitionType.INTEGRATION.value
            if experiment_dao.acquisition_type is None
            else experiment_dao.acquisition_type.value
        )

    def _find_initialization(self, device_uid):
        for initialization in self._recipe["experiment"]["initializations"]:
            if initialization["device_uid"] == device_uid:
                return initialization
        return None

    def add_connectivity_from_experiment(
        self,
        experiment_dao: ExperimentDAO,
        leader_properties: LeaderProperties,
        clock_settings: Dict[str, Any],
    ):
        if leader_properties.global_leader is not None:
            initialization = self._find_initialization(leader_properties.global_leader)
            initialization["config"]["repetitions"] = 1
            initialization["config"]["holdoff"] = 0
            if leader_properties.is_desktop_setup:
                initialization["config"]["triggering_mode"] = "desktop_leader"
        if leader_properties.is_desktop_setup:
            # Internal followers are followers on the same device as the leader. This
            # is necessary for the standalone SHFQC, where the SHFSG part does neither
            # appear in the PQSC device connections nor the DIO connections.
            for f in leader_properties.internal_followers:
                initialization = self._find_initialization(f)
                initialization["config"]["triggering_mode"] = "internal_follower"

        for device in experiment_dao.device_infos():
            device_uid = device.uid
            initialization = self._find_initialization(device_uid)
            reference_clock = experiment_dao.device_reference_clock(device_uid)
            if reference_clock is not None:
                initialization["config"]["reference_clock"] = reference_clock

            if device.device_type == "hdawg" and clock_settings["use_2GHz_for_HDAWG"]:
                initialization["config"][
                    "sampling_rate"
                ] = DeviceType.HDAWG.sampling_rate_2GHz

            if device.device_type == "shfppc":
                ppchannels = []
                for signal in experiment_dao.signals():
                    amplifier_pump = experiment_dao.amplifier_pump(signal)
                    if amplifier_pump is not None and amplifier_pump[0] == device_uid:
                        ppchannels.append(amplifier_pump[1])
                initialization["ppchannels"] = ppchannels

            for follower in experiment_dao.dio_followers():
                initialization = self._find_initialization(follower)
                if leader_properties.is_desktop_setup:
                    initialization["config"]["triggering_mode"] = "desktop_dio_follower"
                else:
                    initialization["config"]["triggering_mode"] = "dio_follower"

        for pqsc_device_id in experiment_dao.pqscs():
            for port in experiment_dao.pqsc_ports(pqsc_device_id):
                follower_device_id = port["device"]
                follower_device_init = self._find_initialization(follower_device_id)
                follower_device_init["config"]["triggering_mode"] = "zsync_follower"

    def add_output(
        self,
        device_id,
        channel,
        offset=0.0,
        diagonal=1.0,
        off_diagonal=0.0,
        precompensation=None,
        modulation=False,
        oscillator=None,
        oscillator_frequency=None,
        lo_frequency=None,
        port_mode=None,
        output_range=None,
        output_range_unit=None,
        port_delay=None,
        scheduler_port_delay=0.0,
        marker_mode=None,
        amplitude=None,
    ):
        output = {"channel": channel, "enable": True}
        if offset is not None:
            output.update({"offset": offset})
        if diagonal is not None and off_diagonal is not None:
            output.update(
                {"gains": {"diagonal": diagonal, "off_diagonal": off_diagonal}}
            )
        if precompensation is not None:
            output["precompensation"] = precompensation
        if lo_frequency is not None:
            output["lo_frequency"] = lo_frequency
        if port_mode is not None:
            output["port_mode"] = port_mode
        if output_range is not None:
            output["range"] = output_range
        if output_range_unit is not None:
            output["range_unit"] = output_range_unit
        if oscillator is not None:
            output["oscillator"] = oscillator
        output["modulation"] = modulation
        if oscillator_frequency is not None and not isinstance(
            oscillator_frequency, ParameterInfo
        ):
            output["oscillator_frequency"] = oscillator_frequency
        if port_delay is not None:
            output["port_delay"] = port_delay
        output["scheduler_port_delay"] = scheduler_port_delay
        if marker_mode is not None:
            output["marker_mode"] = marker_mode
        if amplitude is not None:
            output["amplitude"] = amplitude

        initialization: dict = self._find_initialization(device_id)
        outputs: list = initialization.setdefault("outputs", [])
        outputs.append(output)

    def add_input(
        self,
        device_id,
        channel,
        lo_frequency=None,
        input_range=None,
        input_range_unit=None,
        port_delay=None,
        scheduler_port_delay=0.0,
    ):
        input = {"channel": channel, "enable": True}
        if lo_frequency is not None:
            input["lo_frequency"] = lo_frequency
        if input_range is not None:
            input["range"] = input_range
        if input_range_unit is not None:
            input["range_unit"] = input_range_unit
        if port_delay is not None:
            input["port_delay"] = port_delay
        input["scheduler_port_delay"] = scheduler_port_delay

        initialization: dict = self._find_initialization(device_id)
        inputs: list = initialization.setdefault("inputs", [])
        inputs.append(input)

    def add_awg(
        self,
        device_id: str,
        awg_number: int,
        signal_type: str,
        qa_signal_id: Optional[str],
        command_table_match_offset: Optional[int],
        feedback_register: Optional[int],
    ):
        initialization = self._find_initialization(device_id)

        if "awgs" not in initialization:
            initialization["awgs"] = []
        awg = {
            "awg": awg_number,
            "signal_type": signal_type,
            "qa_signal_id": qa_signal_id,
            "command_table_match_offset": command_table_match_offset,
            "feedback_register": feedback_register,
        }
        initialization["awgs"].append(awg)

    def add_realtime_step(
        self,
        device_id: str,
        awg_id: int,
        seqc_filename: str,
        wave_indices_name: str,
        nt_loop_indices: List[int],
    ):
        self._recipe["experiment"]["realtime_execution_init"].append(
            {
                "device_id": device_id,
                "awg_id": awg_id,
                "seqc_ref": seqc_filename,
                "wave_indices_ref": wave_indices_name,
                "nt_step": {"indices": nt_loop_indices},
            }
        )

    def from_experiment(
        self,
        experiment_dao: ExperimentDAO,
        leader_properties: LeaderProperties,
        clock_settings: Dict[str, Any],
    ):
        self.add_devices_from_experiment(experiment_dao)
        self.add_connectivity_from_experiment(
            experiment_dao, leader_properties, clock_settings
        )
        self.add_acquisition_type_from_experiment(experiment_dao)

    def add_simultaneous_acquires(
        self, simultaneous_acquires: Dict[float, Dict[str, str]]
    ):
        # Keys are of no interest, only order and simultaneity is important
        self._recipe["experiment"]["simultaneous_acquires"] = list(
            simultaneous_acquires.values()
        )

    def add_total_execution_time(self, total_execution_time):
        self._recipe["experiment"]["total_execution_time"] = total_execution_time

    def add_max_step_execution_time(self, add_max_step_execution_time):
        self._recipe["experiment"][
            "max_step_execution_time"
        ] = add_max_step_execution_time

    def recipe(self):
        return self._recipe

    def add_measurements(self, measurement_map):
        for initialization in self._recipe["experiment"]["initializations"]:
            device_uid = initialization["device_uid"]
            if device_uid in measurement_map:
                initialization["measurements"] = measurement_map[device_uid]
