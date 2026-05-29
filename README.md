# shrinking-algorithms

A Python library for reducing the complexity of [PlantUML](https://plantuml.com/) diagrams.
Large architecture or sequence diagrams can become unreadable as a system grows.
`shrinking-algorithms` parses a diagram into a graph, applies a graph-reduction algorithm,
and outputs a simplified PlantUML diagram that preserves the most structurally significant relationships.

[![PyPI version](https://img.shields.io/pypi/v/shrinking-algorithms)](https://pypi.org/project/shrinking-algorithms/)
[![Python](https://img.shields.io/pypi/pyversions/shrinking-algorithms)](https://pypi.org/project/shrinking-algorithms/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Features

- Parse `.puml` / PlantUML source into a graph structure
- Reduce the graph with one of two built-in algorithms
- Reconstruct a valid, simplified PlantUML diagram from the reduced graph
- Node embeddings via node2vec for similarity-aware reduction

## Requirements

- Python >= 3.10, < 3.14

## Installation

```bash
pip install shrinking-algorithms
```

## Usage

```python
from shrinking_algorithms import DiagramShrinker

puml = """
@startuml
A --> B
B --> C
C --> D
D --> A
@enduml
"""

result = DiagramShrinker(puml, algorithm="kruskals").shrink()

print(result.get_result_puml())   # simplified PlantUML string
print(result.get_reduced())       # reduced graph data
print(result.get_parsed())        # intermediate parsed representation
```

To check which algorithms are available at runtime:

```python
DiagramShrinker.get_all_algorithms()
# ['kruskals', 'evol']
```

## Algorithms

### `kruskals` (default)
Builds a minimum spanning tree of the diagram graph using Kruskal's algorithm.
Best for deterministic, fast reduction of diagrams where the most-connected
relationships should be preserved.

### `evol`
Evolutionary (genetic) algorithm that searches for an optimal subgraph over
multiple generations. Slower but may find better reductions on complex diagrams.

Supported params:

| Param | Type | Default | Description |
|---|---|---|---|
| `population` | `int` | — | Number of candidate solutions per generation |
| `iterations` | `int` | — | Number of generations to run |

```python
result = DiagramShrinker(
    puml,
    algorithm="evol",
    population=50,
    iterations=100
).shrink()
```

## Configuration

An optional `config` dict can be passed to fine-tune algorithm behaviour.
When provided, it takes precedence over keyword params:

```python
DiagramShrinker(puml, algorithm="evol", config={"population": 50, "iterations": 100})
```

## Dependencies

| Library | License |
|---|---|
| [numpy](https://numpy.org) | BSD 3-Clause |
| [networkx](https://networkx.org) | BSD 3-Clause |
| [node2vec](https://github.com/eliorc/node2vec) | MIT |

## Development

```bash
git clone https://github.com/shrinking-corp/algorithms.git
cd algorithms
pip install -e ".[dev]"
```

Run tests:

```bash
pytest --cov=shrinking_algorithms tests/
```

Lint and format:

```bash
ruff check src/
ruff format src/
```

## License

MIT — see [LICENSE](LICENSE).
Third-party license notices: [THIRD_PARTY_LICENSES](THIRD_PARTY_LICENSES).

## Authors

- Kristian Rusnak
- Lukas Mihal
- Marek Lichvar
- Artemii Kaliadin
