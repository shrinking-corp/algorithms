from abc import ABC, abstractmethod

class AlgorithmFactory(ABC):
    @abstractmethod
    def get_algorithm(self):
        raise NotImplemented("not implemented")