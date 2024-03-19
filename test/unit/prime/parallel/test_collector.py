from unittest import TestCase, mock
from pytest import raises

from src.prime.parallel.collector import CompleteCollector, LightCollector
from src.prime.parallel.common import Signals

from test.mock.mpi import DummyMPIForCollector


class TestCompleteCollector(TestCase):
    def test_start(self):
        # Given
        until_number = 5
        data_to_return = [
            '2:True',
            '3:True',
            '4:False',
            '5:True'
        ]
        dummy_comm = DummyMPIForCollector(data_to_return)

        # When
        collector = CompleteCollector(comm = dummy_comm)
        prime_number_quantity = collector.start(until_number)

        # Then
        self.assertEqual(prime_number_quantity, 3)
        self.assertEqual(collector.primer_numbers, [2, 3, 5])


class TestLightCollector(TestCase):
    def test_start(self):
        # Given
        number_of_workers = 2
        data_to_return = [
            '2:True',
            '3:True',
            Signals.END_SIGNAL.value,
            Signals.END_SIGNAL.value
        ]
        dummy_comm = DummyMPIForCollector(data_to_return)

        # When
        collector = LightCollector(
            comm = dummy_comm
        )
        prime_number_quantity = collector.start(
            quantity_of_processes = number_of_workers + 2
        )

        # Then
        self.assertEqual(prime_number_quantity, 2)
        self.assertEqual(collector.primer_numbers, [2, 3])
