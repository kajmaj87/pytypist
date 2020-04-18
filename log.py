import logging

logging.basicConfig(
    filename="debug.log",
    filemode="w",
    level=logging.WARN,
    format="%(asctime)s %(levelname)s:%(message)s",
    datefmt="%H:%M:%S",
)

debug = logging.debug
warn = logging.warn
