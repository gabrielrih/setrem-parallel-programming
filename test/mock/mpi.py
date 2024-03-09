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
        pass

    def recv(self, *args, **kwargs):
        # fix it
        pass