from pathlib import Path

from shrinking_algorithms.parsers import PUMLParser


def _build_parser() -> PUMLParser:
    config_path = (
        Path(__file__).resolve().parents[1]
        / "src"
        / "shrinking_algorithms"
        / "parsers"
        / "parser_config.json"
    )
    return PUMLParser(str(config_path))


def test_reparse_file_filters_class_members(tmp_path):
    source = tmp_path / "source.puml"
    output = tmp_path / "output.puml"
    source.write_text(
        """@startuml
class A {
  ' keep comments alone
  +id: int
  +name: str
  +ping(x)
  +pong()
}
class B
class C
A -- B
A --> C
@enduml
"""
    )

    parser = _build_parser()
    parser.reparse_file(
        str(source),
        str(output),
        {
            "classes": {
                "A": {
                    "attributes": [{"name": "name", "visibility": "public"}],
                    "methods": [{"signature": "pong()", "visibility": "public"}],
                },
                "C": {"attributes": [], "methods": []},
            },
            "edges": [
                {"source": "A", "target": "C", "relation": "dependency-right"},
            ],
        },
    )

    assert output.read_text() == (
        "@startuml\n"
        "class A {\n"
        "  ' keep comments alone\n"
        "  +name: str\n"
        "  +pong()\n"
        "}\n"
        "class C\n"
        "A --> C\n"
        "@enduml"
    )


def test_reparse_puml_removes_all_members_when_class_is_empty():
    content = """@startuml
class User {
  -id: UUID
  +login(password: String): bool
}
@enduml
"""

    parser = _build_parser()
    result = parser.reparse_puml(
        content,
        {
            "classes": {"User": {"attributes": [], "methods": []}},
            "edges": [],
        },
    )

    assert result == "@startuml\nclass User {\n}\n@enduml"
