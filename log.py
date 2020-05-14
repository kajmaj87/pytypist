import logging

logging.basicConfig(
    filename="debug.log",
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s.%(msecs)d %(levelname)s %(module)s/%(funcName)s at %(lineno)d: %(message)s",
    datefmt="%H:%M:%S",
)


debug = logging.debug
info = logging.info
warn = logging.warn
