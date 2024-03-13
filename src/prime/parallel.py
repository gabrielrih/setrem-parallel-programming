from mpi4py import MPI
from enum import Enum
from typing import List
from copy import deepcopy, copy

from src.util.converters import StringConverter
from src.util.decorators import timeit, profileit
from src.util.logger import Logger


logger = Logger.get_logger(__name__)


class Rank(Enum):
    EMITTER = 0
    COLLECTOR = 1


class Signals(Enum):
    END_SIGNAL = 'end_signal'


class ParallelManager:
    MIN_OF_PROCESSES = 3  # an emitter, an collector and at least one worker

    def __init__(self, comm = MPI.COMM_WORLD):
        self.comm = comm
        self.quantity_of_processes = self.comm.Get_size()
        self.me = self.comm.Get_rank()  # who am I?

    @profileit
    def run(self, until_number: int):
        if self.me == Rank.EMITTER.value:
            if self.quantity_of_processes < ParallelManager.MIN_OF_PROCESSES:
                raise ValueError(f'You must have at least {str(ParallelManager.MIN_OF_PROCESSES)} processes!')
            logger.info(f'Searching quantity of prime numbers until {until_number}')
            Emitter(self.comm, self.quantity_of_processes).start(until_number)
        elif self.me == Rank.COLLECTOR.value:
            if self.quantity_of_processes < ParallelManager.MIN_OF_PROCESSES: return
            quantity = Collector(self.comm).start(until_number)
            logger.info(f'There are {quantity} prime numbers before {until_number}!')
        else:
            if self.quantity_of_processes < ParallelManager.MIN_OF_PROCESSES: return
            Worker(self.comm, self.me).start()


class Data:
    DELIMITER = ':'

    @staticmethod
    def serialize(number: str, is_prime: bool) -> str:
        data = f'{number}{Data.DELIMITER}{is_prime}'
        return str(data)

    @staticmethod
    def deserialize(data: str):
        raw_data = data.split(Data.DELIMITER)
        number = int(raw_data[0])
        is_prime = StringConverter.string_to_bool(raw_data[1])
        return number, is_prime


class Emitter:
    def __init__(self, comm, quantity_of_processes: int):
        self.comm = comm
        self._workers_rank = Emitter.get_workers_rank(quantity_of_processes)

    @timeit
    def start(self, until_number: int):
        ''' Send work for the workers '''
        logger.debug('Starting the emitter')
        # While there are numbers to check, send work to workers
        workers_rank = copy(self._workers_rank)
        number = 2  # starts by two because this is the first prime number
        req = None
        while number <= until_number:
            if not workers_rank: workers_rank = copy(self._workers_rank)  # rotate the rank
            worker = workers_rank.pop()
            logger.debug(f'Sending data {str(number)} to {worker =}')
            if req: req.wait()
            req = self.comm.isend(obj = str(number), dest = worker)
            number += 1
        # Nothing more to do, it sends a message to the workers to stop processing
        for worker in self._workers_rank:
            logger.debug(f'Sending end_signal to worker {worker}')
            self.comm.send(obj = Signals.END_SIGNAL.value, dest = worker)
        logger.debug('Finishing the emitter')

    @staticmethod
    def get_workers_rank(quantity_of_processes: int) -> List[int]:
        ''' The workers rank are all but the emitter and the collector rank '''
        workers_rank = list()
        for rank in range(quantity_of_processes):
            if rank == Rank.EMITTER.value: continue
            if rank == Rank.COLLECTOR.value: continue
            workers_rank.append(rank)
        logger.debug(f'Workers rank list: {str(workers_rank)}')
        return workers_rank


class Collector:
    def __init__(self, comm):
        self.comm = comm
        self.primer_numbers = list()
        self._data = Data()

    @timeit
    def start(self, until_number: int) -> int:
        ''' Receive all answers from workers and append the prime numbers '''
        logger.debug('Starting the collector')
        expected_responses = until_number - 1
        received_responses = 0
        while received_responses < expected_responses:
            raw_data = self.comm.recv(source = MPI.ANY_SOURCE)  # wait until receive data
            number, is_prime = self._data.deserialize(raw_data)
            if is_prime:
                self.primer_numbers.append(number)
            received_responses += 1
        logger.debug(f'The prime numbers are: {str(self.primer_numbers)}')
        logger.debug('Finishing the collector')
        return len(self.primer_numbers)


class Worker:
    def __init__(self, comm, me):
        self.comm = comm
        self.me = me
        self._data = Data()
        self.numbers_processed = 0

    @timeit
    def start(self):
        ''' Receive numbers and return if it is prime or not '''
        logger.debug(f'Starting the worker {str(self.me)}')
        req = None
        while True:
            # Receive and process data
            data = self.comm.recv(source = Rank.EMITTER.value)  # wait until receive data
            if data == Signals.END_SIGNAL.value:
                break  # It's necessary to break the infinite loop
            is_prime = Worker.is_prime_number(number = int(data))
            logger.debug(f'I am the worker {str(self.me)}. Is {data} prime? {str(is_prime)}')
            # Sending data to collector
            data = self._data.serialize(number = data, is_prime = is_prime)
            if req: req.wait()
            req = self.comm.isend(
                obj = data,
                dest = Rank.COLLECTOR.value  # target
            )
            self.numbers_processed += 1
        logger.debug(f'Finishing the worker {str(self.me)}')

    @staticmethod
    def is_prime_number(number: int) -> bool:
        if number < 2: return False  # The first prime number is 2
        is_prime = True
        antecedent = 2
        while antecedent < number:
            if number % antecedent == 0:  # not prime number
                is_prime = False
                break
            antecedent += 1
        return is_prime
