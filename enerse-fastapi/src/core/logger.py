import logging
import sys


def setup_logging():
    fmt = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=fmt,
        stream=sys.stdout,
    )
    # lower noise from third-party libs if needed:
    logging.getLogger("httpx").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
