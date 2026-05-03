from abc import ABC, abstractmethod
from shrinking_algorithms.algorithms import Algorithm

class AlgorithmCreator(ABC):

    def initialize_and_get_algorithm(self, settings: dict) -> Algorithm:
        algorithm = self.get_algorithm()
        config = self.get_config()
        self.set_instances(algorithm, settings, config)
        return algorithm

    @staticmethod
    @abstractmethod
    def get_algorithm() -> Algorithm:
        raise NotImplemented("not implemented")

    @staticmethod
    @abstractmethod
    def get_config() -> dict:
        raise NotImplemented("not implemented")

    @staticmethod
    @abstractmethod
    def set_instances(algorithm: Algorithm,
                      settings: dict,
                      config: dict
                      ) -> None:
        raise NotImplemented("not implemented")