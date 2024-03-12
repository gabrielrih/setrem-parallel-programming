from typing import Dict

from src.prime.parallel import Rank, Signals


class DummyMPIForManager:
    def __init__(self, parameters: Dict = {}):
        self._parameters = parameters

    def Get_size(self) -> int:
        processes = self._parameters.get('processes')
        if processes is None:
            return 3  # default of minimum processes
        return processes
    
    def Get_rank(self) -> int:
        rank = self._parameters.get('rank')
        if rank is None:
            return Rank.EMITTER.value  # simulating the emitter
        return rank


class DummyMPIForEmitter:
    def send(self, *args, **kwargs):
        return None  # do nothing here


class DummyMPIForCollector:
    def recv(self, *args, **kwargs) -> str:
        return '3:True'  # return always the same value


class DummyMPIForWorker:
    def __init__(self):
        self._received_messages = 0

    def send(self, *args, **kwargs):
        return None  # do nothing here

    def recv(self, *args, **kwargs) -> any:
        # First message, simulating that the worker must calculate if three is a number
        if self._received_messages == 0:
            self._received_messages += 1
            return 3
        # Second message, simulating that the worker must calculate if four is a number
        if self._received_messages == 1:
            self._received_messages += 1
            return 4
        
        # Last message, sending the end signal to stop doing the work
        return Signals.END_SIGNAL.value
