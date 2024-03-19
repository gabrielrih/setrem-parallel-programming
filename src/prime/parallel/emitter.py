from copy import copy
from abc import ABC, abstractmethod

from src.prime.parallel.common import \
    Signals, \
    NumbersSerializer
from src.prime.parallel.worker import Worker
from src.util.logger import Logger


logger = Logger.get_logger(__name__)


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
