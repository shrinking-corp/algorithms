from shrinking_algorithms.algorithms.factories import AlgorithmCreator
from shrinking_algorithms.algorithms import NullAlgorithm

class NullCreator(AlgorithmCreator):

    def get_algorithm(self, settings: dict) -> NullAlgorithm:
        return NullAlgorithm()
