import logging
from typing import Optional


def configure_logger(log_path: Optional[str] = None) -> None:

    log_path = log_path if log_path is not None else 'relevamiento_etl.log'

    logging.basicConfig(level=logging.INFO)

    log = logging.getLogger()

    format_string = (
        f"%(asctime)s|%(levelname)7s|%(filename)s:%(lineno)d|%(funcName)s|%(message)s"
    )
    formatter = logging.Formatter(format_string)

    fh = logging.FileHandler(log_path, "w+")
    sh = logging.StreamHandler(None)

    log.handlers.clear()
    for handler in [fh, sh]:
        handler.setFormatter(formatter)
        log.addHandler(handler)
