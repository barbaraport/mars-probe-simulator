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
        Logger.log(event.value, status="started", **payload)

        if event == ProbeEvents.PROBE_CREATED:
            ProbeMetrics.inc_probe_created()
        elif event == ProbeEvents.PROBE_INVALID_SETUP:
            ProbeMetrics.inc_probe_invalid_setup()
        elif event == ProbeEvents.PROBE_COMMAND_SENT:
            ProbeMetrics.inc_probe_command_sent()
        elif event == ProbeEvents.PROBE_INVALID_COMMAND:
            ProbeMetrics.inc_probe_invalid_command()

        Logger.log(event.value, status="finished", **payload)
