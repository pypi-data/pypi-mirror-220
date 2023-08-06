import unittest

import logging

from mweb.utils.log import hide_secrets

logger = logging.getLogger(__name__)


class TestHideSecrets(unittest.TestCase):
    def test_hide_secrets(self):
        self.assertEqual(
            'https://foo:**********@github.com/example.git',
            hide_secrets("https://foo:bar@github.com/example.git"),
        )


if __name__ == '__main__':
    unittest.main()
