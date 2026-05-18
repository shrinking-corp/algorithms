import json
from shrinking_algorithms.parsers.puml_interpreter import PumlInterpreter
from shrinking_algorithms.parsers.puml_interpreter import FilteredStructureBuilder
from shrinking_algorithms.parsers.puml_interpreter import PumlReconstructor

class PUMLParser:
    def __init__(self, config_path="parser_config.json"):
        self.relations = {}
        self.class_names = set()
        self.parse_config(config_path)

        if not self.relations:
            print("No relations loaded, using default settings.")
            return

    def parse_config(self, config_path):
        if config_path is None:
            print("No config path provided, loading default config.")
            return {}

        try:
            with open(config_path, "r") as file:
                config = json.load(file)
                self.relations = config.get("relations", {})
                self.class_names = set(config.get("class_names", []))
                return config

        except Exception as e:
            print(f"Error reading config file: {e}")
            return {}

    """
    Legacy code, will be removed in future when WebAPP is updated.
    """
    def parse_file(self, filepath) -> dict:

        with open(filepath, "r") as file:
            lines = file.read().splitlines()

        interpreter = PumlInterpreter(
            relations=self.relations,
            class_names=self.class_names,
        )
        return interpreter.parse(lines)

    def parse_puml(self, content: str):
        interpreter = PumlInterpreter(
            relations=self.relations,
            class_names=self.class_names,
        )
        return interpreter.parse(content.splitlines())

    def reparse_file(self, source_path, output_path, new_data):

        if source_path is None or output_path is None:
            print("Source or output path is None.")
            return

        if not new_data:
            print("No new data provided for reparsing.")
            return

        interpreter = PumlInterpreter(
            relations=self.relations,
            class_names=self.class_names,
        )

        with open(source_path, "r") as file:
            source_lines = file.read().splitlines()

        source_data = interpreter.parse(source_lines)
        filtered = FilteredStructureBuilder().build(source_data, new_data)
        output = PumlReconstructor(self.relations).reconstruct(filtered, source_lines)

        with open(output_path, "w") as file:
            file.write(output)


    def reparse_puml(self, content: str, new_data: dict):
        if not content:
            raise TypeError("Original puml content for reparsing is empty.")

        if not new_data:
            raise TypeError("No new data provided for reparsing.")


        interpreter = PumlInterpreter(
            relations=self.relations,
            class_names=self.class_names,
        )

        source_lines = content.strip().split("\n")

        source_data = interpreter.parse(source_lines)
        filtered = FilteredStructureBuilder().build(source_data, new_data)
        output = PumlReconstructor(self.relations).reconstruct(filtered, source_lines)

        return output






