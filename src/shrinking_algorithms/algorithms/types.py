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

def _get_all_algorithm_types() -> list[AlgorithmType]:
    return [alg_type for alg_type in AlgorithmType if alg_type != AlgorithmType.UNKNOWN]