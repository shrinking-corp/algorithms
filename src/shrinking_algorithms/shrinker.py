import json
from typing import TextIO
from .main import process_puml

class DiagramShrinker:
    def __init__(self, algorithm: str, **params):
        self.algorithm = algorithm
        self.params = params

        self._parsed = None
        self._reduced = None
        self._result = None

    def __str__(self):
        return ""

    def shrink(self, file: TextIO) -> "DiagramShrinker":
        self._result = process_puml(file, self.algorithm, json.dumps(self.params))
        return self

    def get_result(self):
        return self._result