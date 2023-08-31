import logging
from logging import *
from logging.handlers import RotatingFileHandler
from rich.logging import RichHandler


"""
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(
            "logs.txt", maxBytes=5000000, backupCount=10
        ),
        logging.StreamHandler(),
    ],
)
"""

basicConfig(
    level=INFO,
    format="%(filename)s:%(lineno)s %(levelname)s: %(message)s",
    datefmt="%m-%d %H:%M",
    handlers=[RichHandler()],
)
console = StreamHandler()
console.setLevel(ERROR)
console.setFormatter(Formatter("%(filename)s:%(lineno)s %(levelname)s: %(message)s"))
getLogger("").addHandler(console)

logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
