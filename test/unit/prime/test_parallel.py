from unittest import TestCase, mock
from pytest import raises

from src.prime.parallel import \
    ParallelManager, \
    Data, \
    Emitter, \
    Collector, \
    Worker, \
    Rank

from test.mock.mpi import \
    DummyMPIForManager, \
    DummyMPIForEmitter, \
    DummyMPIForCollector, \
    DummyMPIForWorker


class TestParallelManager(TestCase):
    def test_min_of_processes(self):
        min_processes = ParallelManager.MIN_OF_PROCESSES
        self.assertEqual(min_processes, 3)

    def test_emitter_when_few_processes(self):
        parameters = {
            'processes': 1,
            'rank': Rank.EMITTER.value
        }
        manager = ParallelManager(comm = DummyMPIForManager(parameters))
        with raises(ValueError):
            manager.run(
                until_number = 10  # it doesn't matter the number here 
            )

    @mock.patch('src.prime.parallel.Emitter.start')
    def test_run_when_emitter(self, mock):
        # Given
        parameters = {
            'processes': 3,
            'rank': Rank.EMITTER.value
        }

        # When
        manager = ParallelManager(
            comm = DummyMPIForManager(parameters)
        )
        manager.run(until_number = 5)  # it doesn't matter the number here

        # Then
        mock.assert_called_once()
        self.assertEqual(manager.quantity_of_processes, parameters['processes'])
        self.assertEqual(manager.me, Rank.EMITTER.value)

    @mock.patch('src.prime.parallel.Collector.start')
    def test_run_when_collector(self, mock):
        # Given
        parameters = {
            'processes': 3,
            'rank': Rank.COLLECTOR.value
        }

        # When
        manager = ParallelManager(
            comm = DummyMPIForManager(parameters)
        )
        manager.run(until_number = 5)  # it doesn't matter the number here

        # Then
        mock.assert_called_once()
        self.assertEqual(manager.quantity_of_processes, parameters['processes'])
        self.assertEqual(manager.me, Rank.COLLECTOR.value)

    @mock.patch('src.prime.parallel.Worker.start')
    def test_run_when_worker(self, mock):
        # Given
        parameters = {
            'processes': 3,
            'rank': 2  # a different from COLLECTOR and EMITTER
        }

        # When
        manager = ParallelManager(
            comm = DummyMPIForManager(parameters)
        )
        manager.run(until_number = 5)  # it doesn't matter the number here

        # Then
        mock.assert_called_once()
        self.assertEqual(manager.quantity_of_processes, parameters['processes'])
        self.assertEqual(manager.me, 2)


class TestData(TestCase):
    def test_serialize(self):
        expected_serialized_data = '10:False'
        data = Data.serialize(10, False)
        self.assertEqual(data, expected_serialized_data)
        self.assertIsInstance(data, str)

    def test_deserialize(self):
        data = '3:True'
        number, is_prime = Data.deserialize(data)
        self.assertEqual(number, 3)
        self.assertEqual(is_prime, True)


class TestEmitter(TestCase):
    def test_get_workers_rank(self):
        expected_workers_rank = [2, 3]
        workers_rank = Emitter.get_workers_rank(
            quantity_of_processes = 4
        )
        self.assertEqual(workers_rank, expected_workers_rank)

    def test_start(self):
        comm = DummyMPIForEmitter()
        emitter = Emitter(comm, 3)
        emitter.start(2)


class TestCollector(TestCase):
    def test_start(self):
        collector = Collector(
            comm = DummyMPIForCollector()
        )
        prime_number_quantity = collector.start(
            until_number = 5
        )
        #  The number 4 is not real, we are just simulating.
        self.assertEqual(prime_number_quantity, 4)


class TestWorker(TestCase):
    def test_when_the_number_is_prime(self):
        is_prime = Worker.is_prime_number(
            number = 3
        )
        self.assertTrue(is_prime)

    def test_when_the_number_isnt_prime(self):
        is_prime = Worker.is_prime_number(
            30
        )
        self.assertFalse(is_prime)

    def test_start(self):
        worker = Worker(comm = DummyMPIForWorker(), me = 1)
        worker.start()
        self.assertEqual(worker.numbers_processed, 2)
