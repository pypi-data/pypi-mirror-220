import logging
import unittest

from mweb.utils import unflatten, flatten

logger = logging.getLogger(__name__)

class TestFlatten(unittest.TestCase):

    def test_flatten(self):
        data = (("tenant_id", "3"), ("id", "4"))
        expected = "tenant_id,3,id,4"
        assert flatten(data) == expected

    def test_unflatten(self):
        data = "tenant_id,3,id,4"
        expected = (("tenant_id", "3"), ("id", "4"))
        assert unflatten(data) == expected
