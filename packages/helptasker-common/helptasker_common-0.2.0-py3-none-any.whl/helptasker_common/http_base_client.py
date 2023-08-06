from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

import httpx
from fastapi.applications import FastAPI
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.trace import get_current_span

from . import __version__
from .logger import cxt_request_id, logger
from .settings import settings
from .trace import tracer_provider


@asynccontextmanager
async def http_base_client(
    base_url: str = '',
    verify: bool = True,
    accept: str = 'application/json',
    app: FastAPI | None = None,
    timeout: float | None = None,
    headers: dict[str, str] | None = None,
) -> AsyncGenerator[httpx.AsyncClient, None]:
    if headers is None:
        headers = {}

    headers['User-Agent'] = f'{settings.app_name}/{__version__}'
    headers['Accept-Language'] = 'en-US,en;q=0.9'
    headers['Accept'] = accept

    if request_id := cxt_request_id.get():
        headers['Request-ID'] = request_id

    client = httpx.AsyncClient(
        limits=httpx.Limits(
            max_keepalive_connections=settings.http_client_max_keepalive_connections,
            max_connections=settings.http_client_max_connections,
        ),
        base_url=base_url,
        http2=True,
        verify=verify,
        headers=headers,
        event_hooks={
            'request': [hook_request],
            'response': [hook_response],
        },
        timeout=timeout or settings.http_client_timeout,
        app=app,
    )

    try:
        with tracer_provider.get_tracer(settings.app_name).start_as_current_span('HTTPX HTTP request') as span:
            span.set_attribute('verify_certificate', verify)
            yield client
    finally:
        await client.aclose()


async def hook_request(request: httpx.Request):
    span = get_current_span()
    span.update_name(f'HTTPX - {request.method} {str(request.url.host)}')

    span.set_attributes(
        attributes={
            SpanAttributes.HTTP_URL: str(request.url),
            SpanAttributes.HTTP_METHOD: request.method,
            'request_id': request.headers.get('Request-ID', 0),
        },
    )  # type: ignore

    logger.info(f'Request http client: {request.method} {request.url} - Waiting for response')


async def hook_response(response: httpx.Response):
    span = get_current_span()
    span.set_attributes(
        attributes={
            SpanAttributes.HTTP_STATUS_CODE: response.status_code,
            SpanAttributes.HTTP_RESPONSE_CONTENT_LENGTH: response.headers.get('content-length', 0),
        },
    )

    request = response.request

    headers = {}
    for header in response.headers:
        headers[header] = response.headers.get(header)
    span.add_event('headers', attributes=headers)

    logger.info(f'Response http client: {request.method} {request.url} - Status {response.status_code}')
