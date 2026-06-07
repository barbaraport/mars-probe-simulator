from typing import Any

from app.core.events import ProbeEvents, ProbeMetrics
from app.core.logging import Logger


class Observability:
    @classmethod
    def emit(
        cls,
        event: ProbeEvents,
        **payload: Any,
    ):
        if event.value == ProbeEvents.PROBE_CREATED.value:
            ProbeMetrics.probe_created()
        elif event.value == ProbeEvents.PROBE_INVALID_SETUP.value:
            ProbeMetrics.probe_invalid_setup()
        elif event.value == ProbeEvents.PROBE_COMMAND_SENT.value:
            ProbeMetrics.probe_command_sent()
        elif event.value == ProbeEvents.PROBE_INVALID_COMMAND.value:
            ProbeMetrics.probe_invalid_command()

        Logger.log(event.value, **payload)
