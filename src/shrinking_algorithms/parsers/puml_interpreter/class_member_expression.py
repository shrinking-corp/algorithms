from shrinking_algorithms.parsers.puml_interpreter.context import InterpreterContext
from shrinking_algorithms.parsers.puml_interpreter.exceptions import PumlParseException
from shrinking_algorithms.parsers.puml_interpreter.expression import Expression
from shrinking_algorithms.parsers.puml_interpreter.types import ClassMemberParser


class ClassMemberExpression(Expression):
    def __init__(self, class_member_parser: ClassMemberParser):
        self.class_member_parser = class_member_parser

    def interpret(self, line: str, line_number: int, context: InterpreterContext) -> bool:
        if not context.in_class_body or not context.current_class:
            return False

        member = self.class_member_parser(line)
        if not member:
            raise PumlParseException("Invalid class member declaration", line_number, line)

        context.add_member(member)
        return True

