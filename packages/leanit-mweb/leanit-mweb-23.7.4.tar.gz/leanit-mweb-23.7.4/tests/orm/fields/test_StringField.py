import unittest

from mweb.orm.exception import ValidationFailedException
from mweb.orm.fields import StringField


class TestStringField(unittest.TestCase):
    def test_min_length(self):
        field = StringField(min_length=3)
        with self.assertRaises(ValidationFailedException):
            field.validate("ab")

    def test_max_length(self):
        field = StringField(max_length=3)
        with self.assertRaises(ValidationFailedException):
            field.validate("abcd")

    def test_alphabet(self):
        field = StringField(alphabet="abc")
        with self.assertRaises(ValidationFailedException):
            field.validate("def")

    def test_choices(self):
        field = StringField(choices=["a", "b"])
        with self.assertRaises(ValidationFailedException):
            field.validate("c")

if __name__ == '__main__':
    unittest.main()