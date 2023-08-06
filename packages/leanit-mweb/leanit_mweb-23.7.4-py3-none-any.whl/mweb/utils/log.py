from __future__ import annotations
import logging
import re

logger = logging.getLogger(__name__)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

def hide_secrets(input_string: str) -> str:
    """
    Hide secrets in a string.

    :param input_string: The string to hide secrets in.
    :type input_string: str

    >>> hide_secrets("https://foo:bar@github.com/example.git")
    'https://foo:**********@github.com/example.git'
    """
    matches = re.findall(r'https://[a-zA-Z0-9]*?:(.*?)@', input_string)
    if matches:
        for match in matches:
            input_string = input_string.replace(match, "**********")
    return input_string
