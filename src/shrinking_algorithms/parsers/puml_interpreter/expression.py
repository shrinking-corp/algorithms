from abc import ABC, abstractmethod

from shrinking_algorithms.parsers.puml_interpreter.context import InterpreterContext


class Expression(ABC):
    @abstractmethod
    def interpret(self, line: str, line_number: int, context: InterpreterContext) -> bool:
        raise NotImplementedError

