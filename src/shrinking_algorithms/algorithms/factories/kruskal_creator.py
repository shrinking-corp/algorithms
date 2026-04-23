from shrinking_algorithms.algorithms.factories import AlgorithmCreator
from shrinking_algorithms.algorithms import KruskalsAlgorithm

class KruskalCreator(AlgorithmCreator):

    def get_algorithm(self, settings: dict) -> KruskalsAlgorithm:
        algorithm = KruskalsAlgorithm()
        algorithm.initialize(**settings)
        return algorithm
