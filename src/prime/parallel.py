from mpi4py import MPI
from enum import Enum
from typing import List


from src.util.logger import Logger


logger = Logger.get_logger(__name__)


class Rank(Enum):
    EMITTER = 0
    COLLECTOR = 1


class ParallelManager:
    MIN_OF_PROCESSES = 3  # an emitter, an collector and at least one worker

    def __init__(self):
        self.comm = MPI.COMM_WORLD
        self.quantity_of_processes = self.comm.Get_size()

    def run(self, until_number: int):
        if self.quantity_of_processes < ParallelManager.MIN_OF_PROCESSES:
            raise ValueError(f'You must have at least {str(ParallelManager.MIN_OF_PROCESSES)} processes!')
        me = self.comm.Get_rank()  # who am I?
        if me == Rank.EMITTER:
            Emitter(self.comm, self.quantity_of_processes).start(until_number)
        elif me == Rank.COLLECTOR:
            Collector(self.comm).start()
        else:
            Worker(self.comm, me).start()


class Emitter:
    def __init__(self, comm, quantity_of_processes: int):
        self.comm = comm
        self._workers_rank = Emitter.get_workers_rank(quantity_of_processes)

    def start(self, until_number: int):
        workers_rank = self._workers_rank
        number = 2  # starts by two because this is the first prime number
        while number <= until_number:
            if not workers_rank: workers_rank = self._workers_rank  # rotate the rank
            worker = workers_rank.pop()  # remove one element
            logger.info(f'Sending data {str(number)} to {worker =}')
            self.comm.send(
                obj = number,  # data
                dest = worker  # traget
            )
            number += 1
        logger.info('Finishing the emitter')

    @staticmethod
    def get_workers_rank(quantity_of_processes: int) -> List[int]:
        ''' The workers rank are all but the emitter and the collector rank '''
        workers_rank = [ rank for rank in range(quantity_of_processes) ]
        workers_rank.remove(Rank.EMITTER)
        workers_rank.remove(Rank.COLLECTOR)
        logger.debug(f'Workers rank {str(workers_rank)}')
        return workers_rank


class Collector:
    def __init__(self, comm):
        self.comm = comm
        self._primer_numbers = list()

    def start(self):
        # While / listening
        # Receive every single response from workers
        #   and append it to the array.
        # Return the array at the end
        # Problem: How to know when to stop the while?
        pass


class Worker:
    def __init__(self, comm, me):
        self.comm = comm
        self.me = me

    def start(self):
        ''' Receive numbers and return if it is prime or not '''
        while True:
            number = self.comm.recv(source = Rank.EMITTER.value)  # wait until receive data
            is_prime = Worker.is_prime_number(number)
            logger.info(f'I am the worker {str(self.me)}. Is {number} prime? {str(is_prime)}')
            # FIX IT
            # Send data to collector

            # FIX IT
            # How to break the loop?
        logger.info(f'Finishing the worker {str(self.me)}')

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
