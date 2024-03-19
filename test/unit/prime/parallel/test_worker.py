from unittest import TestCase

from src.prime.parallel.common import Signals
from src.prime.parallel.worker import \
    Worker, \
    CompleteWorker, \
    LightWorker

from test.mock.mpi import DummyMPIForWorker


class TestWorker(TestCase):
    def test_when_the_number_is_prime(self):
        is_prime = Worker.is_prime_number(
            number = 3
        )
        self.assertTrue(is_prime)

    def test_when_the_number_is_not_prime(self):
        is_prime = Worker.is_prime_number(
            30
        )
        self.assertFalse(is_prime)

    def test_get_number_of_workers(self):
        quantity = Worker.get_number_of_workers(
            quantity_of_processes = 4
        )
        self.assertEqual(quantity, 2)

    def test_get_workers_rank(self):
        workers_rank = Worker.get_workers_rank(
            quantity_of_processes = 4
        )
        self.assertEqual(workers_rank, [2, 3])


class TestCompleteWorker(TestCase):
    def test_start(self):
        # Given
        data_to_return = [
            '2:12',
            '13:23',
            '24:30',
            Signals.END_SIGNAL.value
        ]
        dummy_comm = DummyMPIForWorker(
            data_to_return
        )
        worker = CompleteWorker(
            comm = dummy_comm,
            me = 2
        )
        worker.start()
        self.assertEqual(worker.numbers_processed, 29)


class TestLightWorker(TestCase):
    def test_start(self):
        # Given
        data_to_return = [
            '2:12',
            '13:23',
            '24:30',
            Signals.END_SIGNAL.value
        ]
        dummy_comm = DummyMPIForWorker(
            data_to_return
        )
        worker = LightWorker(
            comm = dummy_comm,
            me = 2
        )
        worker.start()
        self.assertEqual(worker.numbers_processed, 29)
