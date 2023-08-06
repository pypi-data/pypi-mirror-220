# Copyright 2022 Zurich Instruments AG
# SPDX-License-Identifier: Apache-2.0

import logging
from typing import Any, Optional

from laboneq.compiler.experiment_access.pulse_def import PulseDef
from laboneq.compiler.experiment_access.section_info import SectionInfo
from laboneq.compiler.experiment_access.section_signal_pulse import SectionSignalPulse
from laboneq.core.exceptions import LabOneQException
from laboneq.core.types.enums import AcquisitionType
from laboneq.data.compilation_job import ParameterInfo

logger = logging.getLogger(__name__)


class LoaderBase:
    def __init__(self):
        self.acquisition_type: Optional[AcquisitionType] = None

        # leader_uid, follower_uid, port
        self.pqsc_ports: list[tuple[str, str, int]] = []

        # leader_uid, follower_uid
        self.dios: list[tuple[str, str]] = []
        self.global_leader_device_id: str = None

        self._devices = {}
        self._device_oscillators = {}
        self._oscillators = {}
        self._pulses = {}
        self._sections = {}
        self._section_parameters = {}
        self._section_signals = {}
        self._section_signal_pulses = {}
        self._section_tree = {}
        self._servers = {}
        self._signals = {}
        self._signal_connections = {}
        self._signal_markers = {}
        self._signal_oscillator = {}
        self._signal_trigger = {}
        self._root_sections = []
        self._handle_acquires = {}

        self._all_parameters: dict[str, ParameterInfo] = {}

    def data(self) -> dict[str, Any]:
        return {
            "devices": self._devices,
            "device_oscillators": self._device_oscillators,
            "oscillators": self._oscillators,
            "pulses": self._pulses,
            "root_sections": self._root_sections,
            "sections": self._sections,
            "section_parameters": self._section_parameters,
            "section_signals": self._section_signals,
            "section_signal_pulses": self._section_signal_pulses,
            "section_tree": self._section_tree,
            "servers": self._servers,
            "signals": self._signals,
            "signal_connections": self._signal_connections,
            "signal_markers": self._signal_markers,
            "signal_oscillator": self._signal_oscillator,
            "signal_trigger": self._signal_trigger,
            "handle_acquires": self._handle_acquires,
            "global_leader_device_id": self.global_leader_device_id,
        }

    def add_device_oscillator(self, device_id, oscillator_id):
        self._device_oscillators.setdefault(device_id, []).append(
            {
                "device_id": device_id,
                "oscillator_id": oscillator_id,
            }
        )

    def _get_or_create_parameter(self, parameter_id) -> ParameterInfo:
        if (parameter := self._all_parameters.get(parameter_id)) is not None:
            return parameter
        param = self._all_parameters[parameter_id] = ParameterInfo(uid=parameter_id)
        return param

    def add_section_parameter(
        self,
        section_id,
        parameter_id,
        start=None,
        step=None,
        values_list=None,
        axis_name=None,
    ):
        param = self._get_or_create_parameter(parameter_id)
        if (
            param.start is not None
            or param.step is not None
            or param.values is not None
            or param.axis_name is not None
        ):
            raise LabOneQException(
                "Illegal nesting of multiple real-time sweeps over same parameter: {}".format(
                    parameter_id
                )
            )
        param.start = start
        param.step = step
        param.values = values_list
        param.axis_name = axis_name

        self._section_parameters.setdefault(section_id, []).append(param)

    def add_section_signal(self, section_uid, signal_uid):
        self._section_signals.setdefault(section_uid, set()).add(signal_uid)

    def add_section_signal_pulse(
        self, section_id, signal_id, section_signal_pulse: SectionSignalPulse
    ):
        self._section_signal_pulses.setdefault(section_id, {}).setdefault(
            signal_id, []
        ).append(section_signal_pulse)
        if section_signal_pulse.acquire_params is not None:
            handle = section_signal_pulse.acquire_params.handle
            if handle is not None:
                self.add_handle_acquire(handle, signal_id)

    def add_signal_marker(self, signal_id, marker: str):
        self._signal_markers.setdefault(signal_id, set()).add(marker)

    def add_server(self, server_id, host, port, api_level):
        self._servers[server_id] = {
            "id": server_id,
            "port": int(port) if port is not None else None,
            "host": host,
            "api_level": api_level,
        }

    def add_device(
        self,
        device_id,
        device_type,
        reference_clock=None,
        reference_clock_source=None,
        is_qc=None,
    ):
        self._devices[device_id] = {
            "uid": device_id,
            "device_type": device_type,
            "reference_clock": reference_clock,
            "reference_clock_source": reference_clock_source,
            "is_qc": is_qc,
        }

    def add_oscillator(self, oscillator_id, frequency, is_hardware):
        self._oscillators[oscillator_id] = {
            "uid": oscillator_id,
            "frequency": frequency,
            "is_hardware": is_hardware,
        }

    def add_signal(self, signal_id, signal_type, modulation, offset=None):
        self._signals[signal_id] = {
            "signal_id": signal_id,
            "signal_type": signal_type,
            "modulation": modulation,
            "offset": offset,
        }

    def add_signal_oscillator(self, signal_id, oscillator_id):
        self._signal_oscillator[signal_id] = oscillator_id

    def add_signal_connection(self, signal_id, signal_connection):
        self._signal_connections[signal_id] = signal_connection

    def add_section(self, section_id, section_info: SectionInfo):
        if section_info.handle is not None and section_info.user_register is not None:
            raise LabOneQException(
                f"Section {section_id} has both a handle and a user register set."
            )
        self._sections[section_id] = section_info

    def add_pulse(self, pulse_id, pulse_def: PulseDef):
        self._pulses[pulse_id] = pulse_def

    def add_section_child(self, parent_id, child_id):
        self._section_tree.setdefault(parent_id, []).append(child_id)

    def add_handle_acquire(self, handle: str, signal: str):
        if handle in self._handle_acquires:
            other_signal = self._handle_acquires[handle]
            if other_signal != signal:
                raise LabOneQException(
                    f"Acquisition handle '{handle}' used on multiple signals: {other_signal}, {signal}"
                )
        self._handle_acquires[handle] = signal
