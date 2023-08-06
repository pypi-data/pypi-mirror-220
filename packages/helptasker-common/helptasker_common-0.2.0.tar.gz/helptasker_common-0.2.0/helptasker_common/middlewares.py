import time
import traceback
from uuid import uuid4

from fastapi import Request, status
from fastapi.responses import ORJSONResponse
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.trace import Status, StatusCode
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from .context import cxt_api_version, cxt_ip
from .logger import cxt_request_id, logger
from .settings import Environment, settings
from .trace import trace


class Middleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        api_version_token = cxt_api_version.set(0)
        cxt_ip_token = cxt_ip.set('0.0.0.0')
        cxt_request_id_token = cxt_request_id.set(request.headers.get('request-id', str(uuid4())))

        # Timer
        start_timer = time.monotonic()

        # IP
        if ip := request.headers.get('x-real-ip', request.headers.get('x-forwarded-for')):
            cxt_ip_token = cxt_ip.set(ip)

        # API Version
        if 'v1' in request.url.path.split('/', 3):
            api_version_token = cxt_api_version.set(1)
        elif 'v2' in request.url.path.split('/', 3):
            api_version_token = cxt_api_version.set(2)

        path = request.scope.get('path')
        method = request.scope.get('method')
        with trace.get_tracer(settings.app_name).start_as_current_span(f'{method} {path}') as span:
            try:
                response = await call_next(request)
            except Exception as err:
                if settings.environment == Environment.development:  # pragma: no cover
                    traceback.print_exc()

                response = ORJSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content={'error': 'Internal server error'},
                )

                span_status_code = Status(status_code=StatusCode.ERROR, description=f'{err}')
                span.record_exception(exception=err)
            else:
                span_status_code = Status(status_code=StatusCode.OK)

            # Setting the status code
            span.set_status(span_status_code)

            # Setting attributes for trace
            span.set_attributes(
                {
                    SpanAttributes.HTTP_SCHEME: request.scope.get('scheme', 'n/a'),
                    SpanAttributes.HTTP_URL: request.url.path,
                    SpanAttributes.HTTP_CLIENT_IP: cxt_ip.get() or '0.0.0.0',
                    SpanAttributes.HTTP_USER_AGENT: request.headers.get('user-agent', 'n/a'),
                    SpanAttributes.HTTP_METHOD: request.method,
                    SpanAttributes.HTTP_STATUS_CODE: response.status_code,
                    SpanAttributes.HTTP_RESPONSE_CONTENT_LENGTH: int(response.headers.get('content-length', 0)),
                    'api.version': cxt_api_version.get(),
                    'request_id': cxt_request_id.get() or '',
                },
            )

            # Adding the header Request-ID server response
            response.headers['Request-ID'] = cxt_request_id.get() or ''

            # Adding the header Trace-ID server response
            if not span.get_span_context().trace_id == 0:
                response.headers['Trace-ID'] = format(span.get_span_context().trace_id, '032x')

            if request.url.path not in ['/metrics', '/healthcheck/']:
                extra = {
                    'method': request.method,
                    'user-agent': request.headers.get('user-agent', 'n/a'),
                    'ip': request.headers.get('x-real-ip', request.headers.get('x-forwarded-for', '127.0.0.1')),
                    'uri': request.url.path,
                    'response_status_code': response.status_code,
                    'request_duration_seconds': round(time.monotonic() - start_timer, 3),
                }

                if query := request.url.query:
                    extra['query'] = query

                logger.info(msg=f'{request.method} {request.url.path}', extra=extra)

        # Reset context var
        cxt_ip.reset(cxt_ip_token)
        cxt_api_version.reset(api_version_token)
        cxt_request_id.reset(cxt_request_id_token)
        return response
