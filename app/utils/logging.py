import sys
import structlog
import logging


def setup_logging() -> None:
    disable_uvicorn_logs()
    configure_structlog()


def disable_uvicorn_logs() -> None:
    uvicorn_error = logging.getLogger("uvicorn.error")
    uvicorn_error.disabled = True
    uvicorn_access = logging.getLogger("uvicorn.access")
    uvicorn_access.disabled = True


def configure_structlog() -> None:
    # logging.basicConfig(level=logging.DEBUG)
    shared_processors = [
        # Processors that have nothing to do with output,
        # e.g., add timestamps or log level names.
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M.%S"),
        structlog.processors.StackInfoRenderer(),
    ]
    if sys.stderr.isatty():
        # Pretty printing when we run in a terminal session.
        # Automatically prints pretty tracebacks when "rich" is installed
        log_level = logging.DEBUG
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer(),
        ]
    else:
        # Print JSON when we run, e.g., in a Docker container.
        # Also print structured tracebacks.
        log_level = logging.INFO
        processors = shared_processors + [
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ]
    structlog.configure(
        processors,
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
    )
