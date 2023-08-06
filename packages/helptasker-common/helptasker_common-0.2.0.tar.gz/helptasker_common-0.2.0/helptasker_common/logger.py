import logging
import sys
from contextvars import ContextVar

from opentelemetry.trace import get_current_span
from pythonjsonlogger import jsonlogger

from .settings import settings

cxt_request_id: ContextVar[str | None] = ContextVar('request_id', default=None)

logger = logging.getLogger(settings.log_name)


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)

        log_record['level'] = record.levelname
        log_record['logger'] = record.name

        if request_id := cxt_request_id.get():
            log_record['request_id'] = request_id

        current_span = get_current_span()
        if not current_span.get_span_context().trace_id == 0:
            log_record['span_id'] = format(current_span.get_span_context().span_id, '016x')
            log_record['trace_id'] = format(current_span.get_span_context().trace_id, '032x')


class InfoFilter(logging.Filter):
    def filter(self, rec):  # noqa: A003
        return rec.levelno in (logging.DEBUG, logging.INFO)


def logger_init() -> logging.Logger:
    formatter = CustomJsonFormatter()

    # StreamHandler
    handler_stream_stdout = logging.StreamHandler(sys.stdout)
    handler_stream_stderr = logging.StreamHandler(sys.stderr)

    handler_stream_stdout.setLevel(logging.DEBUG)
    handler_stream_stderr.setLevel(logging.WARNING)

    handler_stream_stdout.setFormatter(formatter)
    handler_stream_stderr.setFormatter(formatter)

    handler_stream_stdout.addFilter(InfoFilter())

    log = logging.getLogger(settings.log_name)
    log.setLevel(settings.log_level.upper())
    log.addHandler(handler_stream_stdout)
    log.addHandler(handler_stream_stderr)

    return log
