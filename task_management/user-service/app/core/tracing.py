from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
# from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor 

import os
from loguru import logger  # <--- 1. Import Loguru

def setup_tracing(app):
    service_name = os.getenv("OTEL_SERVICE_NAME", "unknown-service")
    otel_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://tempo:4317")

    try:
        # 2. Tạo Resource
        resource = Resource.create(attributes={
            "service.name": service_name
        })

        tracer_provider = TracerProvider(resource=resource)
        
        trace.set_tracer_provider(tracer_provider)
        otlp_exporter = OTLPSpanExporter(endpoint=otel_endpoint, insecure=True)
        
        span_processor = BatchSpanProcessor(otlp_exporter)
        tracer_provider.add_span_processor(span_processor)

        FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer_provider)
        
        RequestsInstrumentor().instrument()
        
        logger.success(f"🕵️ Tracing enabled for {service_name} -> {otel_endpoint}")

    except Exception as e:
        logger.error(f"❌ Failed to setup tracing: {e}")