from typing import List
from abc import ABC, abstractmethod

from src.prime.parallel.common import \
    Rank, \
    Signals, \
    NumbersSerializer, \
    IsPrimeSerializer
from src.util.logger import Logger


logger = Logger.get_logger(__name__)


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
            data = self.comm.recv(source = Rank.EMITTER.value)  # wait until receives data
            if data == Signals.END_SIGNAL.value:
                logger.debug(f'Sending end_signal to collector')
                self.comm.send(
                    obj = Signals.END_SIGNAL.value,
                    dest = Rank.COLLECTOR.value
                )
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
                self.comm.send(
                    obj = data,
                    dest = Rank.COLLECTOR.value  # target
                )
                from_number += 1
                self.numbers_processed += 1
        logger.debug(f'Finishing the worker {str(self.me)}')
