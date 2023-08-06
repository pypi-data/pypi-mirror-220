import os
from enum import Enum
from functools import cached_property
from pathlib import Path
from typing import Literal

from pydantic import PostgresDsn, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LogLevel(str, Enum):
    """A class for determining logging levels"""

    debug: str = 'DEBUG'
    info: str = 'INFO'
    warning: str = 'WARNING'
    fatal: str = 'FATAL'


class Environment(str, Enum):
    """A class for determining environments"""

    development: str = 'DEVELOPMENT'
    testing: str = 'TESTING'
    production: str = 'PRODUCTION'


class Scheme(str, Enum):
    http: str = 'http'
    https: str = 'https'


class Settings(BaseSettings):
    app_name: str = 'FastID - Common'
    """ Application name """

    log_name: str = app_name
    """Logger name"""

    log_level: LogLevel = LogLevel.info
    """ Logging level """

    environment: Environment = Environment.production
    """ Environment """

    # Http client
    http_client_timeout: int = 10
    """HTTP defaults to including reasonable timeouts for all network operations, while Requests has no timeouts by
    default."""

    http_client_max_keepalive_connections: int = 5
    """ Number of allowable keep-alive connections """

    http_client_max_connections: int = 10
    """ Maximum number of allowable connections """

    # Tempo server
    opentelemetry_enable: bool = False
    """ Enables or disables sending """

    opentelemetry_scheme: Scheme = Scheme.http
    """Tempo scheme http or https"""

    opentelemetry_host: str = 'tempo'
    """Tempo host address as one of the following: an IP address or a domain name"""

    opentelemetry_port: int = 4317
    """Port number to connect to at the server host"""


settings = Settings()
