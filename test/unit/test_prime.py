from unittest import TestCase

from src.prime import quantity_of_prime_numbers


class TestPrime(TestCase):
    def test_quantity_of_prime_numbers_when_one(self):
        ''' Do not enter in the first while loop '''
        # Given
        max_number = 1
        expected_quantity_of_prime_numbers = 0
        # When
        quantity = quantity_of_prime_numbers(max_number)
        # Then
        self.assertEqual(quantity, expected_quantity_of_prime_numbers)

    def test_quantity_of_prime_numbers_when_two(self):
        ''' Enter in the first while loop but not in the second one '''
        # Given
        max_number = 2
        expected_quantity_of_prime_numbers = 1
        # When
        quantity = quantity_of_prime_numbers(max_number)
        # Then
        self.assertEqual(quantity, expected_quantity_of_prime_numbers)

    def test_quantity_of_prime_numbers_when_third(self):
        ''' Full code coverage for the method
            Prime numbers between 1 and 30:
            2, 3, 5, 7, 11, 13, 17, 19, 23, 29
        '''
        # Given
        max_number = 30
        expected_quantity_of_prime_numbers = 10
        # When
        quantity = quantity_of_prime_numbers(max_number)
        # Then
        self.assertEqual(quantity, expected_quantity_of_prime_numbers)
