from __future__ import annotations
import logging

from starlette.requests import Request

from mweb.state.client import ClientState

logger = logging.getLogger(__name__)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

def fetch_state(request: Request) -> ClientState:
    state = ClientState.from_request(request)
    return state
