from unittest import TestCase, mock

from src.prime.sequential import SequentialManager


class TestSequentialManager(TestCase):
    @mock.patch('src.prime.sequential.SequentialManager.quantity_of_prime_numbers')
    def test_run(self, mock):
        SequentialManager.run(until_number = 10)  # it doesn't matter the number here
        mock.is_called_once()

    def test_quantity_of_prime_numbers_when_last_then_two(self):
        # Given
        until_number = 1
        expected_quantity_of_prime_numbers = 0
        # When
        quantity = SequentialManager.quantity_of_prime_numbers(until_number)
        # Then
        self.assertEqual(quantity, expected_quantity_of_prime_numbers)

    def test_quantity_of_prime_numbers_when_two(self):
        # Given
        until_number = 2
        expected_quantity_of_prime_numbers = 1
        # When
        quantity = SequentialManager.quantity_of_prime_numbers(until_number)
        # Then
        self.assertEqual(quantity, expected_quantity_of_prime_numbers)

    def test_quantity_of_prime_numbers_when_third(self):
        # Given
        until_number = 30
        # Prime numbers: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29
        expected_quantity_of_prime_numbers = 10
        # When
        quantity = SequentialManager.quantity_of_prime_numbers(until_number)
        # Then
        self.assertEqual(quantity, expected_quantity_of_prime_numbers)
