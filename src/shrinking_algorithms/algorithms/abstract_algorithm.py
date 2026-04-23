from abc import ABC, abstractmethod
from typing import Any, Dict

class Algorithm(ABC):
    """
    Interface for all diagram-shrinking algorithms.
    """

    @abstractmethod
    def compute(self, parsed_puml: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the algorithm on parsed PUML data and return the reduced PUML data.
        """
        raise NotImplemented("compute method not implemented")