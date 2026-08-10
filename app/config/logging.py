import logging
import sys

def setup_logging(level: str = "INFO") -> None:
    """
    Configure applocation-wide logging.
    """

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ],
        force=True
    )

def get_logger(name: str) -> logging.Logger:
    """
    Rerturn a logger for the given module.
    """
    return logging.getLogger(name)