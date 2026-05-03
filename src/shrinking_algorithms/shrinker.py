from shrinking_algorithms.algorithms import AlgorithmType, Factory, map_to_algorithm_type, get_all_algorithm_types
from shrinking_algorithms.parsers import PUMLParser

from typing import Optional, Union, Self
from pathlib import Path

import os

class DiagramShrinker:
    """
    Initialize the DiagramShrinker with an algorithm and its parameters.

    :param algorithm: The shrinking algorithm to use. Must be one of
        ``"kruskals"`` or ``"evol"``.
    :param config: The config used for shrinking PlantUML diagrams as a dict.
    :param params: Additional keyword arguments passed to the algorithm.
        For ``"evol"``, supported params are ``population`` (int) and
        ``iterations`` (int).
    """
    def __init__(self,
                 puml_content: str,
                 algorithm: Union[str, AlgorithmType] = None,
                 config: Optional[dict] = None,
                 **params
                 ) -> None:
        self._puml_content: str = puml_content
        self._config: Optional[dict] = config if config else params
        self._algorithm: AlgorithmType = map_to_algorithm_type(algorithm)

        self._parsed = None
        self._reduced = None
        self._result_puml = None

    def shrink(self) -> Self:
        """
        Shrink the given PlantUML diagram.

        Reads the content of the opened file, runs it through the configured
        algorithm, and stores the results on the instance. Returns ``self``
        to allow method chaining.

        :returns: The instance itself, allowing chained getter calls.
        :raises TypeError: If the file cannot be parsed or the algorithm is unknown.
        :raises RuntimeError: If an unexpected error occurs during processing.
        """
        current_dir = Path(__file__).resolve().parent
        config_path = current_dir / "parsers" / "parser_config.json"
        parser = PUMLParser(str(config_path))

        try:
            parsed = parser.parse_file(self._puml_content)
            if not parsed:
                raise TypeError("Unable to parse PUML file")

            creator = Factory.get_creator(self._algorithm)
            algorithm = creator.initialize_and_get_algorithm(self._config)
            reduced = algorithm.compute(parsed)

            result_puml_list = parser.reparse_file(self._puml_content, reduced)
            result_puml_str = "\n".join(result_puml_list)

            self._parsed = parsed
            self._reduced = reduced
            self._result_puml = result_puml_str

            return self

        except Exception as e:
            raise RuntimeError(e.__str__())

    def get_all(self) -> dict[str, Optional[str]]:
        """
        Return all results as a dictionary.

        :returns: A dict with keys ``"parsed"``, ``"reduced"``, and
            ``"result_puml"``. Values are ``None`` if shrink() has not been called yet.
        """
        return {
            "parsed": self._parsed,
            "reduced": self._reduced,
            "result_puml": self._result_puml
        }

    def get_parsed(self) -> Optional[str]:
        """
        Return the intermediate parsed representation of the diagram.

        :returns: The parsed PUML data, or ``None`` if shrink() has not been called yet.
        """
        return self._parsed

    def get_reduced(self) -> Optional[str]:
        """
        Return the reduced graph data produced by the algorithm.

        :returns: The reduced data, or ``None`` if shrink() has not been called yet.
        """
        return self._reduced

    def get_result_puml(self) -> Optional[str]:
        """
        Return the final shrunk PlantUML diagram as a string.

        :returns: The result PUML string, or ``None`` if shrink() has not been called yet.
        """
        return self._result_puml

    def get_config(self) -> Optional[dict]:
        """
        Return the config used for shrinking PlantUML diagrams as a dict.

        :returns: The config used for shrinking PlantUML diagrams as a dict.
        """
        return self._config

    @staticmethod
    def get_all_algorithms() -> list[str]:
        algorithms = get_all_algorithm_types()
        return [alg.value for alg in algorithms]