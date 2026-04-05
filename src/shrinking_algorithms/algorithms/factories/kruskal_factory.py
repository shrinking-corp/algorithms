from shrinking_algorithms.algorithms import AlgorithmFactory
from shrinking_algorithms.algorithms import KruskalsAlgorithm

class KruskalFactory(AlgorithmFactory):

    def get_algorithm(self):
        return KruskalsAlgorithm()