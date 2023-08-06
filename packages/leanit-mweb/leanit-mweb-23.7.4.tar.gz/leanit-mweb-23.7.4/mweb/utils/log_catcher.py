from __future__ import annotations
import logging
from io import StringIO

logger = logging.getLogger(__name__)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class LogCatcher(object):
    formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(name)-12s %(message)s", datefmt='%Y-%m-%d %H:%M:%S')

    def __init__(self):
        self.stream = StringIO()
        self.handler = logging.StreamHandler(self.stream)
        self.handler.setFormatter(self.formatter)

    def __enter__(self):
        logging.getLogger().addHandler(self.handler)
        return self

    def __exit__(self, type, value, traceback):
        logging.getLogger().removeHandler(self.handler)

    def get(self) -> str:
        self.stream.seek(0)
        return self.stream.read()


# usage
with LogCatcher() as catcher:
    logger.info("baz")
    print(catcher.get())  # prints sth. like: "2022-05-19 15:04:12 INFO     __main__ baz"