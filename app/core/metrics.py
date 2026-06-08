from prometheus_client import Counter

probe_created_total = Counter(
    "probe_created_total",
    "Total number of probes created",
)

probe_invalid_setups_total = Counter(
    "probe_invalid_setups_total",
    "Total number of invalid probe setups",
)

probe_commands_total = Counter(
    "probe_commands_total", "Total number of commands sent to probes"
)

probe_invalid_commands_total = Counter(
    "probe_invalid_commands_total",
    "Total number of invalid commands sent to probes",
)
