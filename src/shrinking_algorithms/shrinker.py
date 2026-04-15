from shrinking_algorithms.main import process_puml

from typing import TextIO, Optional
import json

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
    def __init__(self, algorithm: str, config: dict = None, **params):
        self.algorithm = algorithm
        self.config = config if config else params

        self._parsed = None
        self._reduced = None
        self._result_puml = None

    def shrink(self, content: str) -> "DiagramShrinker":
        """
        Shrink the given PlantUML diagram.

        Reads the content of the opened file, runs it through the configured
        algorithm, and stores the results on the instance. Returns ``self``
        to allow method chaining.

        :param content: The PlantUML diagram as a string.
        :returns: The instance itself, allowing chained getter calls.
        :raises TypeError: If the file cannot be parsed or the algorithm is unknown.
        :raises RuntimeError: If an unexpected error occurs during processing.
        """
        result = process_puml(content, self.algorithm, json.dumps(self.config))

        self._parsed = result.get("parsed")
        self._reduced = result.get("reduced")
        self._result_puml = result.get("result_puml")

        return self

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

    def get_config(self) -> dict:
        """
        Return the config used for shrinking PlantUML diagrams as a dict.

        :returns: The config used for shrinking PlantUML diagrams as a dict.
        """
        return self.params

    def set_config(self, config: dict = None, **params):
        """
        Set the config used for shrinking PlantUML diagrams.

        :param config: The config used for shrinking PlantUML diagrams as a dict.
        :param params: Additional keyword arguments passed to the algorithm.
        """
        self.config = config if config else params