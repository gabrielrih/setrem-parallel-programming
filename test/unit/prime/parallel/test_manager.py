from unittest import TestCase, mock
from pytest import raises

from src.prime.parallel.common import \
    Rank
from src.prime.parallel.manager import \
    CompleteParallelManager, \
    LightParallelManager

from test.mock.mpi import DummyMPIForManager


class TestCompleteParallelManager(TestCase):
    def test_min_of_processes(self):
        min_processes = CompleteParallelManager.MIN_OF_PROCESSES
        self.assertEqual(min_processes, 3)

    def test_emitter_when_few_processes(self):
        parameters = {
            'processes': 1,
            'rank': Rank.EMITTER.value
        }
        manager = CompleteParallelManager(comm = DummyMPIForManager(parameters))
        with raises(ValueError):
            manager.run(
                until_number = 5,
                batch_size = 50
            )  # it doesn't matter the number here

    @mock.patch('src.prime.parallel.emitter.CompleteEmitter.start')
    def test_run_when_emitter(self, mock):
        # Given
        parameters = {
            'processes': 3,
            'rank': Rank.EMITTER.value
        }

        # When
        manager = CompleteParallelManager(
            comm = DummyMPIForManager(parameters)
        )
        manager.run(
            until_number = 5,
            batch_size = 50
        )  # it doesn't matter the number here

        # Then
        mock.assert_called_once()
        self.assertEqual(manager.quantity_of_processes, parameters['processes'])
        self.assertEqual(manager.me, Rank.EMITTER.value)

    @mock.patch('src.prime.parallel.collector.CompleteCollector.start')
    def test_run_when_collector(self, mock):
        # Given
        parameters = {
            'processes': 3,
            'rank': Rank.COLLECTOR.value
        }

        # When
        manager = CompleteParallelManager(
            comm = DummyMPIForManager(parameters)
        )
        manager.run(
            until_number = 5,
            batch_size = 50
        )  # it doesn't matter the number here

        # Then
        mock.assert_called_once()
        self.assertEqual(manager.quantity_of_processes, parameters['processes'])
        self.assertEqual(manager.me, Rank.COLLECTOR.value)

    @mock.patch('src.prime.parallel.worker.CompleteWorker.start')
    def test_run_when_worker(self, mock):
        # Given
        parameters = {
            'processes': 3,
            'rank': 2  # a different from COLLECTOR and EMITTER
        }

        # When
        manager = CompleteParallelManager(
            comm = DummyMPIForManager(parameters)
        )
        manager.run(
            until_number = 5,
            batch_size = 50
        )  # it doesn't matter the number here

        # Then
        mock.assert_called_once()
        self.assertEqual(manager.quantity_of_processes, parameters['processes'])
        self.assertEqual(manager.me, 2)


class TestLightParallelManager(TestCase):
    def test_min_of_processes(self):
        min_processes = LightParallelManager.MIN_OF_PROCESSES
        self.assertEqual(min_processes, 3)

    def test_emitter_when_few_processes(self):
        parameters = {
            'processes': 1,
            'rank': Rank.EMITTER.value
        }
        manager = LightParallelManager(comm = DummyMPIForManager(parameters))
        with raises(ValueError):
            manager.run(
                until_number = 5,
                batch_size = 50
            )  # it doesn't matter the number here

    @mock.patch('src.prime.parallel.emitter.CompleteEmitter.start')
    def test_run_when_emitter(self, mock):
        # Given
        parameters = {
            'processes': 3,
            'rank': Rank.EMITTER.value
        }

        # When
        manager = LightParallelManager(
            comm = DummyMPIForManager(parameters)
        )
        manager.run(
            until_number = 5,
            batch_size = 50
        )  # it doesn't matter the number here

        # Then
        mock.assert_called_once()
        self.assertEqual(manager.quantity_of_processes, parameters['processes'])
        self.assertEqual(manager.me, Rank.EMITTER.value)

    @mock.patch('src.prime.parallel.collector.LightCollector.start')
    def test_run_when_collector(self, mock):
        # Given
        parameters = {
            'processes': 3,
            'rank': Rank.COLLECTOR.value
        }

        # When
        manager = LightParallelManager(
            comm = DummyMPIForManager(parameters)
        )
        manager.run(
            until_number = 5,
            batch_size = 50
        )  # it doesn't matter the number here

        # Then
        mock.assert_called_once()
        self.assertEqual(manager.quantity_of_processes, parameters['processes'])
        self.assertEqual(manager.me, Rank.COLLECTOR.value)

    @mock.patch('src.prime.parallel.worker.LightWorker.start')
    def test_run_when_worker(self, mock):
        # Given
        parameters = {
            'processes': 3,
            'rank': 2  # a different from COLLECTOR and EMITTER
        }

        # When
        manager = LightParallelManager(
            comm = DummyMPIForManager(parameters)
        )
        manager.run(
            until_number = 5,
            batch_size = 50
        )  # it doesn't matter the number here

        # Then
        mock.assert_called_once()
        self.assertEqual(manager.quantity_of_processes, parameters['processes'])
        self.assertEqual(manager.me, 2)
