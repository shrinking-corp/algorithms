from __future__ import annotations

from typing import Any, Dict

from shrinking_algorithms.algorithms.preprocessing.preprocess_base import (
    PreprocessStep,
)
from shrinking_algorithms.algorithms.preprocessing.decorator_base import (
    AlgorithmDecorator,
)


class PreprocessingDecorator(AlgorithmDecorator):
    def __init__(
        self,
        wrapped,
        steps: list[PreprocessStep],
        **params: Any,
    ) -> None:
        self.steps = steps
        super().__init__(wrapped, **params)

    def compute(self, parsed_puml: Dict[str, Any]) -> Dict[str, Any]:
        result = parsed_puml
        for step in self.steps:
            result = step.apply(result)
        return self.wrapped.compute(result)
