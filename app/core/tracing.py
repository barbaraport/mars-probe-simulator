from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from app.core.config import settings


def tracing_config():
    resource = Resource.create(
        {
            "service.name": "mars-probe-simulator",
            "service.version": "1.0.0",
            "deployment.environemnt": settings.ENV,
        }
    )
    processor = BatchSpanProcessor(
        OTLPSpanExporter(endpoint="http://otel-collector:4318/v1/traces")
    )
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(processor)

    trace.set_tracer_provider(provider)
