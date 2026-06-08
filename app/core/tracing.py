from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def tracing_config():
    resource = Resource.create({"service.name": "mars-probe-simulator"})
    processor = BatchSpanProcessor(
        OTLPSpanExporter(endpoint="http://jaeger:4318/v1/traces")
    )
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(processor)

    trace.set_tracer_provider(provider)
