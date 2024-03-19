from unittest import TestCase, mock
from pytest import raises

from src.prime.parallel.common import \
    IsPrimeSerializer, \
    NumbersSerializer


class TestIsPrimeSerializer(TestCase):
    def test_serialize(self):
        expected_serialized_data = '10:False'
        data = IsPrimeSerializer.serialize(10, False)
        self.assertEqual(data, expected_serialized_data)
        self.assertIsInstance(data, str)

    def test_deserialize(self):
        data = '3:True'
        number, is_prime = IsPrimeSerializer.deserialize(data)
        self.assertEqual(number, 3)
        self.assertEqual(is_prime, True)


class TestNumbersSerializer(TestCase):
    def test_serialize(self):
        expected_serialized_data = '2:12'
        data = NumbersSerializer.serialize(
            from_number = 2,
            to_number = 12)
        self.assertEqual(data, expected_serialized_data)
        self.assertIsInstance(data, str)

    def test_deserialize(self):
        data = '2:12'
        from_number, to_number = NumbersSerializer.deserialize(data)
        self.assertEqual(from_number, 2)
        self.assertEqual(to_number, 12)
