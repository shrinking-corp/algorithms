from typing import Any, Dict
from shrinking_algorithms.algorithms.abstract_algorithm import Algorithm

class NullAlgorithm(Algorithm):
    """
    Use no algorithm for diagram shrinking. Useful for serving as a wrappee for 
    the Preprocessing decorator utilizing Null Object pattern. 
    """
    def compute(self, parsed_puml: Dict[str, Any]) -> Dict[str, Any]:
        return parsed_puml