import os
from collections.abc import Callable, Coroutine
from functools import wraps
from typing import Any, ParamSpec, TypeVar

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

from .settings import settings

resource = Resource(attributes={'service.name': settings.app_name})

trace.set_tracer_provider(TracerProvider(resource=resource))

devnull = open(os.devnull, 'w')
processor = BatchSpanProcessor(ConsoleSpanExporter(out=devnull))

if settings.opentelemetry_enable:  # pragma: no cover
    processor = BatchSpanProcessor(
        OTLPSpanExporter(
            endpoint=f'{settings.opentelemetry_scheme.value}://'
            f'{settings.opentelemetry_host}:{settings.opentelemetry_port}',
        ),
    )

tracer_provider: TracerProvider = trace.get_tracer_provider()  # type: ignore
tracer_provider.add_span_processor(processor)

P = ParamSpec('P')
T = TypeVar('T')


def decorator_trace(name: str = 'n/a'):
    """
    Decorator for the function, supports asynchronous functions,
    allows you to create a span inside the parent
        Example:
        .. code-block:: python
            @decorator_trace()
    """

    def decorator(function: Callable[P, Coroutine[Any, Any, T]]) -> Callable[P, Coroutine[Any, Any, T]]:
        @wraps(function)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            with trace.get_tracer(settings.app_name).start_as_current_span(name):
                return await function(*args, **kwargs)

        return wrapper

    return decorator
