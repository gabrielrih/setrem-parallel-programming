from mpi4py import MPI
from enum import Enum
from typing import List, Dict
from copy import deepcopy

from src.util.converters import StringConverter
from src.util.logger import Logger


logger = Logger.get_logger(__name__)


class Rank(Enum):
    EMITTER = 0
    COLLECTOR = 1


class Signals(Enum):
    END_SIGNAL = 'end_signal'


class ParallelManager:
    MIN_OF_PROCESSES = 3  # an emitter, an collector and at least one worker

    def __init__(self):
        self.comm = MPI.COMM_WORLD
        self.quantity_of_processes = self.comm.Get_size()

    def run(self, until_number: int):
        if self.quantity_of_processes < ParallelManager.MIN_OF_PROCESSES:
            raise ValueError(f'You must have at least {str(ParallelManager.MIN_OF_PROCESSES)} processes!')
        me = self.comm.Get_rank()  # who am I?
        if me == Rank.EMITTER.value:
            Emitter(self.comm, self.quantity_of_processes).start(until_number)
        elif me == Rank.COLLECTOR.value:
            Collector(self.comm).start(until_number)
        else:
            Worker(self.comm, me).start()


class Data:
    DELIMITER = ':'

    @staticmethod
    def serialize(number: int, is_prime: bool) -> str:
        return f'{str(number)}{str(Data.DELIMITER)}{str(is_prime)}'

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

    def start(self, until_number: int):
        ''' Send work for the workers '''
        logger.debug('Starting the emitter')
        # While there are numbers to check, send work to workers
        workers_rank = deepcopy(self._workers_rank)
        number = 2  # starts by two because this is the first prime number
        while number <= until_number:
            if not workers_rank: workers_rank = deepcopy(self._workers_rank)  # rotate the rank
            worker = workers_rank.pop()
            data = str(number)
            logger.info(f'Sending data {data} to {worker =}')
            self.comm.send(obj = data, dest = worker)
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
        self._primer_numbers = list()
        self._data = Data()

    def start(self, until_number: int):
        ''' Receive all answers from workers and append the prime numbers '''
        logger.debug(f'Starting the collector')
        expected_responses = until_number - 1
        received_responses = 0
        while received_responses < expected_responses:
            raw_data = self.comm.recv(source = MPI.ANY_SOURCE)  # wait until receive data
            number, is_prime = self._data.deserialize(raw_data)
            if is_prime: self._primer_numbers.append(number)
            received_responses += 1
        logger.debug(f'The prime numbers are: {str(self._primer_numbers)}')
        logger.info(f'There are {len(self._primer_numbers)} prime numbers before {until_number}!')
        logger.debug(f'Finishing the collector')


class Worker:
    def __init__(self, comm, me):
        self.comm = comm
        self.me = me
        self._data = Data()

    def start(self):
        ''' Receive numbers and return if it is prime or not '''
        logger.debug(f'Starting the worker {str(self.me)}')
        while True:
            # Receive and process data
            data = self.comm.recv(source = Rank.EMITTER.value)  # wait until receive data
            if data == Signals.END_SIGNAL.value: break  # It's necessary to break the infinite loop
            number = int(data)
            is_prime = Worker.is_prime_number(number)
            logger.debug(f'I am the worker {str(self.me)}. Is {str(number)} prime? {str(is_prime)}')
            # Sending data to collector
            data = self._data.serialize(number, is_prime)
            self.comm.send(
                obj = data,
                dest = Rank.COLLECTOR.value  # target
            )
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
