from mpi4py import MPI
from abc import ABC, abstractmethod

from src.prime.parallel.common import \
    Signals, \
    IsPrimeSerializer
from src.prime.parallel.worker import Worker
from src.util.decorators import timeit
from src.util.logger import Logger


logger = Logger.get_logger(__name__)


class Collector(ABC):
    def __init__(self, comm):
        self.comm = comm
        self.primer_numbers = list()
        self._serializer = IsPrimeSerializer()

    @abstractmethod
    def start(*args, **kwargs): pass


class CompleteCollector(Collector):
    @timeit
    def start(self, until_number: int) -> int:
        ''' Receive all answers from workers and append the prime numbers '''
        logger.debug('Starting the collector')
        expected_responses = until_number - 1
        received_responses = 0
        while received_responses < expected_responses:
            data = self.comm.recv(source = MPI.ANY_SOURCE)  # wait until receive data
            number, is_prime = self._serializer.deserialize(data)
            if is_prime:
                self.primer_numbers.append(number)
            received_responses += 1
        logger.debug(f'The prime numbers are: {str(self.primer_numbers)}')
        logger.debug('Finishing the collector')
        return len(self.primer_numbers)


class LightCollector(Collector):
    @timeit
    def start(self, quantity_of_processes: int):
        ''' Receive just the prime numbers from workers '''
        logger.debug('Starting the collector')
        number_of_workers = Worker.get_number_of_workers(quantity_of_processes)
        received_end_signals = 0
        while True:
            data = self.comm.recv(source = MPI.ANY_SOURCE)  # wait until receive data
            if data == Signals.END_SIGNAL.value:
                received_end_signals += 1
                if received_end_signals != number_of_workers:
                    continue  # go back to while loop until it receives end signal from all workers
                break  # It's necessary to break the infinite loop
            number, _ = self._serializer.deserialize(data)
            self.primer_numbers.append(number)
        logger.debug(f'The prime numbers are: {str(self.primer_numbers)}')
        logger.debug('Finishing the collector')
        return len(self.primer_numbers)
