from abc import ABC
from typing import Any, Dict

from shrinking_algorithms.algorithms.abstract_algorithm import Algorithm


class AlgorithmDecorator(Algorithm, ABC):
    def __init__(self, wrapped: Algorithm, **params: Any) -> None:
        self.wrapped = wrapped
        super().__init__(**params)

    def initialize(self, **params: Any) -> None:
        self.wrapped.initialize(**params)

    def compute(self, parsed_puml: Dict[str, Any]) -> Dict[str, Any]:
        return self.wrapped.compute(parsed_puml)
