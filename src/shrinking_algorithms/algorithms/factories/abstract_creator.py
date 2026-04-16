from abc import ABC, abstractmethod
from shrinking_algorithms.algorithms import Algorithm

class AlgorithmCreator(ABC):
    @abstractmethod
    def get_algorithm(self, settings: dict) -> Algorithm:
        raise NotImplemented("not implemented")