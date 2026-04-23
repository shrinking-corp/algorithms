from shrinking_algorithms.algorithms import AlgorithmType
from shrinking_algorithms.algorithms.factories import (
    AlgorithmCreator,
    KruskalCreator,
    EvolCreator,
    NullCreator
)

class Factory():

    @staticmethod
    def get_creator(algorithm: AlgorithmType) -> "AlgorithmCreator":
        if algorithm == AlgorithmType.KRUSKAL:
            return KruskalCreator()
        elif algorithm == AlgorithmType.EVOLUTION:
            return EvolCreator()
        elif algorithm == AlgorithmType.PREPROCESS_ONLY:
            return NullCreator()
        else:
            return KruskalCreator()
