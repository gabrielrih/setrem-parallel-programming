from typing import Dict, List

from src.prime.parallel.common import Rank


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
    
    def isend(self, *args, **kwargs):
        return None  # do nothing here
    
    def wait(self, *args, **kwargs):
        return None  # do nothing here


class DummyMPIForCollector:
    def __init__(self, data_to_return: List):
        self._data = data_to_return
        self._returned_element = 0

    def recv(self, *args, **kwargs) -> str:
        data = self._data[self._returned_element]
        self._returned_element += 1
        return data


class DummyMPIForWorker:
    def __init__(self, data_to_return = List):
        self._data = data_to_return
        self._returned_element = 0

    def send(self, *args, **kwargs):
        return None  # do nothing here

    def isend(self, *args, **kwargs):
        return None  # do nothing here
    
    def wait(self, *args, **kwargs):
        return None  # do nothing here
    
    def recv(self, *args, **kwargs) -> any:
        data = self._data[self._returned_element]
        self._returned_element += 1
        return data
