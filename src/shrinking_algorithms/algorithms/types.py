from enum import StrEnum

class AlgorithmType(StrEnum):
    EVOLUTION = "evol"
    KRUSKAL = "kruskals"
    UNKNOWN = "unknown"
    PREPROCESS_ONLY = "preprocess"

def map_to_algorithm_type(algorithm: str) -> AlgorithmType:
    try:
        return AlgorithmType(algorithm)
    except ValueError:
        return AlgorithmType.UNKNOWN

def get_all_algorithm_types() -> list[AlgorithmType]:
    return [alg_type for alg_type in AlgorithmType if alg_type != AlgorithmType.UNKNOWN]
