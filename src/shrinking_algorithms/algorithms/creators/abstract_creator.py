from abc import ABC, abstractmethod
from shrinking_algorithms.algorithms import Algorithm

class AlgorithmCreator(ABC):

    def create_algorithm(self, settings: dict) -> Algorithm:
        algorithm = self.create_instance()
        config = self.load_default_config()
        self.set_hyperparameters(algorithm, settings, config)
        return algorithm

    @staticmethod
    @abstractmethod
    def create_instance() -> Algorithm:
        raise NotImplementedError("Method in abstract class that's not implemented.")

    @staticmethod
    @abstractmethod
    def load_default_config() -> dict:
        raise NotImplementedError("Method in abstract class that's not implemented.")

    @staticmethod
    @abstractmethod
    def set_hyperparameters(algorithm: Algorithm,
                            settings: dict,
                            config: dict
                            ) -> None:
        raise NotImplementedError("Method in abstract class that's not implemented.")