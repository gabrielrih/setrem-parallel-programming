from typing import Dict


class DummyMPI:
    def __init__(self, parameters: Dict):
        self._parameters = parameters

    def Get_size(self) -> int:
        return self._parameters['processes']
    
    def Get_rank(self) -> int:
        return self._parameters['rank']

    def send(self, *args, **kwargs):
        # fix it
        # for emitter, it don't need to do anything
        # for collector, it doesn't matter
        # for worker, it don't need to do anything
        pass

    def recv(self, *args, **kwargs):
        # fix it
        # for emitter, it doesn't matter
        # for collector, it must receive a raw_data
        # for worker, it must receive a number as a data and then receive a END_SIGNAL to finish the execution
        pass