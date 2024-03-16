from mpi4py import MPI
from enum import Enum
from typing import List
from copy import copy
from abc import ABC, abstractmethod

from src.util.converters import StringConverter
from src.util.decorators import timeit
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

    def run(self, until_number: int, batch_size: int, light_way: bool):
        if self.me == Rank.EMITTER.value:
            if self.quantity_of_processes < ParallelManager.MIN_OF_PROCESSES:
                raise ValueError(f'You must have at least {str(ParallelManager.MIN_OF_PROCESSES)} processes!')
            logger.info(f'Searching quantity of prime numbers until {until_number} ({batch_size =})')
            CompleteEmitter(self.comm, self.quantity_of_processes, batch_size).start(until_number)
        elif self.me == Rank.COLLECTOR.value:
            if self.quantity_of_processes < ParallelManager.MIN_OF_PROCESSES: return
            if light_way:
                quantity = LightCollector(self.comm).start(self.quantity_of_processes)
            else:
                quantity = CompleteCollector(self.comm).start(until_number)
            logger.info(f'There are {quantity} prime numbers before {until_number}!')
        else:
            if self.quantity_of_processes < ParallelManager.MIN_OF_PROCESSES: return
            if light_way:
                LightWorker(self.comm, self.me).start()
                return
            CompleteWorker(self.comm, self.me).start()


class IsPrimeSerializer:
    DELIMITER = ':'

    @staticmethod
    def serialize(number: str, is_prime: bool) -> str:
        data = f'{number}{IsPrimeSerializer.DELIMITER}{is_prime}'
        return str(data)

    @staticmethod
    def deserialize(data: str):
        raw_data = data.split(IsPrimeSerializer.DELIMITER)
        number = int(raw_data[0])
        is_prime = StringConverter.string_to_bool(raw_data[1])
        return number, is_prime


class NumbersSerializer:
    DELIMITER = ':'

    @staticmethod
    def serialize(from_number: int, to_number: int) -> str:
        data = f'{from_number}{NumbersSerializer.DELIMITER}{to_number}'
        return str(data)

    @staticmethod
    def deserialize(data: str):
        raw_data = data.split(NumbersSerializer.DELIMITER)
        from_number = int(raw_data[0])
        to_number = int(raw_data[1])
        return from_number, to_number


class Emitter(ABC):
    def __init__(self, comm, quantity_of_processes: int, batch_size: int):
        self.comm = comm
        self._workers_rank = Worker.get_workers_rank(quantity_of_processes)
        self._batch_size = batch_size  # using it to reduce the communication overhead
        self._serializer = NumbersSerializer()

    @abstractmethod
    def start(self, until_number: int): pass


class CompleteEmitter(Emitter):
    def start(self, until_number: int):
        ''' Send work for the workers '''
        logger.debug('Starting the emitter')
        # While there are numbers to check, send work to workers
        workers_rank = copy(self._workers_rank)
        from_number = 2  # starts by two because this is the first prime number
        req = None
        while from_number <= until_number:
            if not workers_rank: workers_rank = copy(self._workers_rank)  # rotate the rank
            worker = workers_rank.pop()
            to_number = from_number + self._batch_size
            if to_number > until_number: to_number = until_number
            data = self._serializer.serialize(from_number, to_number)
            logger.debug(f'Sending data {data} to {worker =}')
            if req: req.wait()
            req = self.comm.isend(obj = data, dest = worker)
            from_number = to_number + 1
        # Nothing more to do, it sends a message to the workers to stop processing
        for worker in self._workers_rank:
            logger.debug(f'Sending end_signal to worker {worker}')
            self.comm.send(
                obj = Signals.END_SIGNAL.value,
                dest = worker
            )
        logger.debug('Finishing the emitter')


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
                if received_end_signals == number_of_workers:
                    break  # It's necessary to break the infinite loop
            number, _ = self._serializer.deserialize(data)
            self.primer_numbers.append(number)
        logger.debug(f'The prime numbers are: {str(self.primer_numbers)}')
        logger.debug('Finishing the collector')
        return len(self.primer_numbers)
    

class Worker(ABC):
    def __init__(self, comm, me):
        self.comm = comm
        self.me = me
        self.numbers_processed = 0
        self._emitter_serializer = NumbersSerializer()
        self._collector_serializer = IsPrimeSerializer()

    @abstractmethod
    def start(self): pass

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
    
    @staticmethod
    def get_number_of_workers(quantity_of_processes: int) -> int:
        return quantity_of_processes - 2  # emitter and collector
    
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


class CompleteWorker(Worker):
    def start(self):
        ''' Receive numbers and return if it is prime or not '''
        logger.debug(f'Starting the worker {str(self.me)}')
        req = None
        while True:
            # Receive and process data
            data = self.comm.recv(source = Rank.EMITTER.value)  # wait until receive data
            if data == Signals.END_SIGNAL.value:
                break  # It's necessary to break the infinite loop
            from_number, to_number = self._emitter_serializer.deserialize(data)

            while from_number <= to_number:
                is_prime = Worker.is_prime_number(number = from_number)
                logger.debug(f'I am the worker {str(self.me)}. Is {str(from_number)} prime? {str(is_prime)}')
                # Sending data to collector
                data = self._collector_serializer.serialize(
                    number = int(from_number),
                    is_prime = is_prime
                )
                if req: req.wait()
                req = self.comm.isend(
                    obj = data,
                    dest = Rank.COLLECTOR.value  # target
                )
                from_number += 1
                self.numbers_processed += 1
        logger.debug(f'Finishing the worker {str(self.me)}')


class LightWorker(Worker):
    def start(self):
        ''' Receive numbers and send the prime ones to collector '''
        logger.debug(f'Starting the worker {str(self.me)}')
        while True:
            # Receive and process data
            data = self.comm.recv(source = Rank.EMITTER.value)  # wait until receive data
            if data == Signals.END_SIGNAL.value:
                break  # It's necessary to break the infinite loop
            from_number, to_number = self._emitter_serializer.deserialize(data)

            while from_number <= to_number:
                is_prime = Worker.is_prime_number(number = from_number)
                logger.debug(f'I am the worker {str(self.me)}. Is {str(from_number)} prime? {str(is_prime)}')
                if not is_prime:  # in the light way there is no need to send not prime numbers to collector
                    from_number += 1
                    self.numbers_processed += 1
                    continue

                # Sending data to collector
                data = self._collector_serializer.serialize(
                    number = int(from_number),
                    is_prime = is_prime
                )
                #if req: req.wait()
                self.comm.send(
                    obj = data,
                    dest = Rank.COLLECTOR.value  # target
                )
                from_number += 1
                self.numbers_processed += 1
        # Nothing more to do, it sends a message to the collector to stop processing
        logger.debug(f'Sending end_signal to collector')
        self.comm.send(
            obj = Signals.END_SIGNAL.value,
            dest = Rank.COLLECTOR.value
        )
        logger.debug(f'Finishing the worker {str(self.me)}')
