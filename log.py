import logging

logging.basicConfig(
    filename="debug.log",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s:%(message)s",
    datefmt="%H:%M:%S",
)

debug = logging.debug
