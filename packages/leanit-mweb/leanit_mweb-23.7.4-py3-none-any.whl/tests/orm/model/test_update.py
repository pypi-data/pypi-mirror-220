import unittest
from typing import Dict

from mweb.orm.fields import IntegerField, StringField
from mweb.orm.model import Model


class TestUpdate(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        class User(Model):
            _table = "user"
            _pk = ["id"]

            id = IntegerField()
            name = StringField()
            age = IntegerField()

        User._initialize()
        cls.User = User

    def test_build_update_query_and_values(self):
        # Test case 1: Single field update
        query_doc = {'id': 1}
        update_doc = {'name': 'John'}
        expected_query = 'UPDATE "user" SET name=%s WHERE id=%s'
        expected_args = ['John', 1]
        result = self.User._build_update_query_and_values(query_doc, update_doc)
        self.assertEqual(result, [expected_query, expected_args])

        # Test case 2: Multiple field update
        query_doc = {'id': 1}
        update_doc = {'name': 'John', 'age': 25}
        expected_query = 'UPDATE "user" SET name=%s,age=%s WHERE id=%s'
        expected_args = ['John', 25, 1]
        result = self.User._build_update_query_and_values(query_doc, update_doc)
        self.assertEqual(result, [expected_query, expected_args])

    def test_get_update_query_and_values(self):
        # Test case 1: Single field update
        instance = self.User(id=1, name='Foo', age=25)
        update_doc = {'name': 'John'}
        expected_query = 'UPDATE "user" SET name=%s WHERE id=%s'
        expected_args = ['John', 1]
        result = instance._get_update_query_and_values(update_doc)
        self.assertEqual(result, [expected_query, expected_args])

if __name__ == '__main__':
    unittest.main()
