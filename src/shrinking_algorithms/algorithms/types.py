from enum import StrEnum

class AlgorithmType(StrEnum):
    EVOLUTION = "evol"
    KRUSKAL = "kruskals"
    UNKNOWN = "unknown"

def _map_to_algorithm_type(algorithm: str) -> AlgorithmType:
    try:
        return AlgorithmType(algorithm)
    except ValueError:
        return AlgorithmType.UNKNOWN