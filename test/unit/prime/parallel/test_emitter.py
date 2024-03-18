from unittest import TestCase

from src.prime.parallel.emitter import CompleteEmitter
from test.mock.mpi import DummyMPIForEmitter



class TestCompleteEmitter(TestCase):
    def test_start(self):
        comm = DummyMPIForEmitter()
        emitter = CompleteEmitter(
            comm,
            quantity_of_processes = 3,
            batch_size = 50)
        emitter.start(2)
