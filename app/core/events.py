from enum import Enum

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
    def probe_created():
        probe_created_total.inc()

    @staticmethod
    def probe_command_sent():
        probe_commands_total.inc()

    @staticmethod
    def probe_invalid_setup():
        probe_invalid_setups_total.inc()

    @staticmethod
    def probe_invalid_command():
        probe_invalid_commands_total.inc()
