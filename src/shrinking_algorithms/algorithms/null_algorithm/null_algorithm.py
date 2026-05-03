from typing import Any, Dict
from shrinking_algorithms.algorithms.abstract_algorithm import Algorithm

class NullAlgorithm(Algorithm):
    """
    Use no algorithm for diagram shrinking. Useful for serving as a wrappee for
    the Preprocessing decorator utilizing Null Object pattern.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def compute(self, parsed_puml: Dict[str, Any]) -> Dict[str, Any]:
        return parsed_puml