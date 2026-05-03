from shrinking_algorithms.algorithms.creators import AlgorithmCreator
from shrinking_algorithms.algorithms import KruskalsAlgorithm

from pathlib import Path
import json

class KruskalCreator(AlgorithmCreator):

    @staticmethod
    def get_algorithm() -> KruskalsAlgorithm:
        return KruskalsAlgorithm()

    @staticmethod
    def get_config() -> dict:
        current_file = Path(__file__).resolve()
        parent_dir = current_file.parent.parent
        config_file = parent_dir / "kruskal" / "kruskals_config.json"

        with (open(config_file, "r", encoding="utf-8") as file):
            config = json.load(file)

        return config

    @staticmethod
    def set_instances(algorithm: KruskalsAlgorithm,
                      settings: dict,
                      config: dict
                      ) -> None:
        algorithm.weights_map = config
        algorithm.PUML = None
        algorithm.size = 0
        algorithm.edges = []
        algorithm.vertex_data = []