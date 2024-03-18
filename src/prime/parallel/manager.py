from mpi4py import MPI
from abc import ABC, abstractmethod

from src.prime.parallel.emitter import CompleteEmitter
from src.prime.parallel.collector import CompleteCollector, LightCollector
from src.prime.parallel.worker import CompleteWorker, LightWorker
from src.prime.parallel.common import Rank
from src.util.logger import Logger


logger = Logger.get_logger(__name__)


class ManagerModel(ABC):
    MIN_OF_PROCESSES = 3  # an emitter, an collector and at least one worker

    def __init__(self, comm = MPI.COMM_WORLD):
        self.comm = comm
        self.quantity_of_processes = self.comm.Get_size()
        self.me = self.comm.Get_rank()  # who am I?

    @abstractmethod
    def run(self, until_number: int, batch_size: int): pass


class CompleteParallelManager(ManagerModel):
    def run(self, until_number: int, batch_size: int):
        if self.me == Rank.EMITTER.value:
            if self.quantity_of_processes < ManagerModel.MIN_OF_PROCESSES:
                raise ValueError(f'You must have at least {str(ManagerModel.MIN_OF_PROCESSES)} processes!')
            logger.info(f'Searching quantity of prime numbers until {until_number} ({batch_size =})')
            CompleteEmitter(self.comm, self.quantity_of_processes, batch_size).start(until_number)
        elif self.me == Rank.COLLECTOR.value:
            if self.quantity_of_processes < ManagerModel.MIN_OF_PROCESSES: return
            quantity = CompleteCollector(self.comm).start(until_number)
            logger.info(f'There are {quantity} prime numbers before {until_number}!')
        else:
            if self.quantity_of_processes < ManagerModel.MIN_OF_PROCESSES: return
            CompleteWorker(self.comm, self.me).start()


class LightParallelManager(ManagerModel):
    def run(self, until_number: int, batch_size: int, light_way: bool):
        if self.me == Rank.EMITTER.value:
            if self.quantity_of_processes < ManagerModel.MIN_OF_PROCESSES:
                raise ValueError(f'You must have at least {str(ManagerModel.MIN_OF_PROCESSES)} processes!')
            logger.info(f'Searching quantity of prime numbers until {until_number} ({batch_size =})')
            CompleteEmitter(self.comm, self.quantity_of_processes, batch_size).start(until_number)
        elif self.me == Rank.COLLECTOR.value:
            if self.quantity_of_processes < ManagerModel.MIN_OF_PROCESSES: return
            quantity = LightCollector(self.comm).start(self.quantity_of_processes)
            logger.info(f'There are {quantity} prime numbers before {until_number}!')
        else:
            if self.quantity_of_processes < ManagerModel.MIN_OF_PROCESSES: return
            LightWorker(self.comm, self.me).start()
