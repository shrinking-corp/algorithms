from shrinking_algorithms.algorithms.factories import AlgorithmCreator
from shrinking_algorithms.algorithms import EvolAlgorithm

class EvolCreator(AlgorithmCreator):

    def get_algorithm(self, settings: dict) -> EvolAlgorithm:
        algorithm = EvolAlgorithm()

        population = settings.get("population")
        iterations = settings.get("iterations")

        algorithm.initialize(
            population_size= population if population else 50,
            generations= iterations if iterations else 100
        )

        return algorithm