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
        config = {}

        with (open(config_file, "r", encoding="utf-8") as file):
            config = json.load(file).get("weights")

        return config

    @staticmethod
    def set_instances(algorithm: KruskalsAlgorithm,
                      settings: dict,
                      config: dict
                      ) -> None:
        """
        Initialize the algorithm with parameters.

        Supported settings:
        - config_path: path to JSON config file with weights mapping
        - Edge weights:
        * dependency 
        * extension 
        * implementation 
        * association 
        * aggregation 
        * composition
        """
        algorithm.weights_map = config
        algorithm.PUML = None
        algorithm.size = 0
        algorithm.edges = []
        algorithm.vertex_data = []

        weights = {}

        weights["dependency"] = settings.get("dependency", algorithm.weights_map["dependency"])
        weights["extension"] = settings.get("extension", algorithm.weights_map["extension"])
        weights["implementation"] = settings.get("implementation", algorithm.weights_map["implementation"])
        weights["association"] = settings.get("association", algorithm.weights_map["association"])
        weights["aggregation"] = settings.get("aggregation", algorithm.weights_map["aggregation"])
        weights["composition"] = settings.get("composition", algorithm.weights_map["composition"])

        algorithm.weights_map = weights
