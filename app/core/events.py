from enum import Enum

from app.core.logging import Logger
from app.core.metrics import (
    probe_created_total,
    probe_invalid_setups_total,
    probe_commands_total,
    probe_invalid_commands_total,
)


class ProbeEvents(Enum):
    PROBE_CREATED = "probe_created"
    PROBE_COMMAND_SENT = "probe_command_sent"
    PROBE_INVALID_SETUP = "probe_invalid_setup"
    PROBE_INVALID_COMMAND = "probe_invalid_command"


class ProbeMetrics:
    @staticmethod
    def inc_probe_created():
        probe_created_total.inc()
        Logger.log(
            "probe_created_total",
            operation="increment",
            new_value=probe_created_total._value.get(),
        )

    @staticmethod
    def inc_probe_command_sent():
        probe_commands_total.inc()
        Logger.log(
            "probe_commands_total",
            operation="increment",
            new_value=probe_commands_total._value.get(),
        )

    @staticmethod
    def inc_probe_invalid_setup():
        probe_invalid_setups_total.inc()
        Logger.log(
            "probe_invalid_setups_total",
            operation="increment",
            new_value=probe_invalid_setups_total._value.get(),
        )

    @staticmethod
    def inc_probe_invalid_command():
        probe_invalid_commands_total.inc()
        Logger.log(
            "probe_invalid_commands_total",
            operation="increment",
            new_value=probe_invalid_commands_total._value.get(),
        )
