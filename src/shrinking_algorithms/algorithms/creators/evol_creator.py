from shrinking_algorithms.algorithms.creators import AlgorithmCreator
from shrinking_algorithms.algorithms import EvolAlgorithm
from pathlib import Path
import json

class EvolCreator(AlgorithmCreator):

    @staticmethod
    def get_algorithm() -> EvolAlgorithm:
        return EvolAlgorithm()

    @staticmethod
    def get_config() -> dict:
        current_file = Path(__file__).resolve()
        parent_dir = current_file.parent.parent
        config_file = parent_dir / "evol" / "ga_config.json"

        with (open(config_file, "r", encoding="utf-8") as file):
            config = json.load(file)

        return config

    @staticmethod
    def set_instances(algorithm: EvolAlgorithm,
                      settings: dict,
                      config: dict
                      ) -> None:
        population_size = settings.get(
            "population_size",
            config.get("population_size")
        )
        generations = settings.get(
            "generations",
            config.get("generations")
        )
        algorithm.mutation_rate = settings.get(
            "mutation_rate",
            config.get("mutation_rate")
        )
        algorithm.crossover_rate = settings.get(
            "crossover_rate",
            config.get("crossover_rate")
        )
        algorithm.exclusion_threshold = settings.get(
            "exclusion_threshold",
            config.get("exclusion_threshold")
        )
        algorithm.inclusion_threshold = settings.get(
            "inclusion_threshold",
            config.get("inclusion_threshold")
        )
        upper_limit = config.get("upper_limit")
        lower_limit = config.get("lower_limit")

        algorithm.population_size = max(
            lower_limit,
            min(upper_limit, population_size)
        )
        algorithm.generations = max(
            lower_limit,
            min(upper_limit, generations)
        )

        algorithm.elements = []
        algorithm.element_types = []
        algorithm.population = []
        algorithm.best_individual = None
        algorithm.best_fitness = -float("inf")
        algorithm.original_embedding = None
        algorithm.G_full = None

        scores = config.get("fitness").get("scores")
        total = sum(scores.values())

        if total <= 0:
            raise ValueError("Scores must sum to a positive value")

        algorithm.scores = {k: (v / total) for k, v in scores.items()}