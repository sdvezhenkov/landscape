import logging
import sys

logger = logging.getLogger('landscape')

_handler = logging.StreamHandler(
    sys.stderr,
)
_handler.setFormatter(
    logging.Formatter(
        '%(levelname)s: %(name)s: %(message)s',
    ),
)

logger.handlers.clear()
logger.addHandler(_handler)
logger.setLevel(logging.INFO)
logger.propagate = False
