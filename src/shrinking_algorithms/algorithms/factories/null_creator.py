from shrinking_algorithms.algorithms.factories import AlgorithmCreator
from shrinking_algorithms.algorithms import NullAlgorithm

class NullCreator(AlgorithmCreator):

    @staticmethod
    def get_algorithm() -> NullAlgorithm:
        return NullAlgorithm()

    @staticmethod
    def get_config() -> dict:
        return {}

    @staticmethod
    def set_instances(algorithm: NullAlgorithm,
                      settings: dict,
                      config: dict
                      ) -> None:
        pass