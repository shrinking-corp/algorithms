from shrinking_algorithms.algorithms import AlgorithmFactory
from shrinking_algorithms.algorithms import EvolAlgorithm

class EvolFactory(AlgorithmFactory):

    def get_algorithm(self):
        return EvolAlgorithm()