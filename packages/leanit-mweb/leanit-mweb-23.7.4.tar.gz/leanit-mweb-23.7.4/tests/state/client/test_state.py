import datetime
import logging
import unittest
from unittest.mock import patch, Mock

from starlette.responses import Response

logger = logging.getLogger(__name__)


class ClientStateCase(unittest.TestCase):
    @patch("mweb.config", {"mweb": {
        "secret_key": "test",
        "jwt": {
            "public_key": """-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE6oVF1eles3nKzfa/NLFoM1nuTUWI
izzS2tvut8jZZxMYtetc4LVauBv31BcU9DD3fa8s/Hh0tbDJu1fi5mCG1A==
-----END PUBLIC KEY-----""",
            "private_key": """-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIPqxJaut1WS3rNRi4hhODZ+Rxn1noVf6bkhkLChsu9h5oAoGCCqGSM49
AwEHoUQDQgAE6oVF1eles3nKzfa/NLFoM1nuTUWIizzS2tvut8jZZxMYtetc4LVa
uBv31BcU9DD3fa8s/Hh0tbDJu1fi5mCG1A==
-----END EC PRIVATE KEY-----"""
        }
    }})
    def test_state(self):
        from mweb.state.client import ClientState

        state = ClientState()
        state.cookie_name = "c"

        state["test"] = "test"
        self.assertEqual(state["test"], "test")

        response = Response()

        state.update_response(response)

        set_cookie_header = response.headers["set-cookie"]
        self.assertTrue(set_cookie_header.startswith("c="))
        set_cookie_value = set_cookie_header.split(";")[0].split("=")[1]

        request = Mock()
        request.cookies = {"c": set_cookie_value}

        state2 = ClientState.from_request(request)
        self.assertEqual(state2["test"], "test")

        # check if cookie_name persists
        self.assertEqual(state2.cookie_name, "c")



if __name__ == '__main__':
    unittest.main()
