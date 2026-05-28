from shrinking_algorithms.algorithms.creators import AlgorithmCreator
from shrinking_algorithms.algorithms import NullAlgorithm

class NullCreator(AlgorithmCreator):

    @staticmethod
    def create_instance() -> NullAlgorithm:
        return NullAlgorithm()

    @staticmethod
    def load_default_config() -> dict:
        return {}

    @staticmethod
    def set_hyperparameters(algorithm: NullAlgorithm,
                      settings: dict,
                      config: dict
                      ) -> None:
        pass