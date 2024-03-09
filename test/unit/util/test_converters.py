from unittest import TestCase

from src.util.converters import StringConverter

class TestStringConverter(TestCase):
    def test_string_to_bool_when_true_lower(self):
        output = StringConverter().\
            string_to_bool('true')
        self.assertEqual(output, True)
        self.assertIsInstance(output, bool)

    def test_string_to_bool_when_true_upper(self):
        output = StringConverter().\
            string_to_bool('TRUE')
        self.assertEqual(output, True)
        self.assertIsInstance(output, bool)

    def test_string_to_bool_when_as_bool_format(self):
        output = StringConverter().\
            string_to_bool('True')
        self.assertEqual(output, True)
        self.assertIsInstance(output, bool)

    def test_string_to_bool_when_false(self):
        output = StringConverter().\
            string_to_bool('false')
        self.assertEqual(output, False)
        self.assertIsInstance(output, bool)      