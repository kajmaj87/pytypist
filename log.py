import logging

logging.basicConfig(
    filename="debug.log",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(module)s.%(funcName)s:%(lineno)d: %(message)s",
    datefmt="%H:%M:%S",
)

debug = logging.debug
info = logging.info
warn = logging.warn
