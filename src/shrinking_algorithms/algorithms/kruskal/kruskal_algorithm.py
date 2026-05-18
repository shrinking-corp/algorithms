from typing import Any, Dict
from shrinking_algorithms.algorithms.abstract_algorithm import Algorithm


class KruskalsAlgorithm(Algorithm):
    """
    Kruskal's MST algorithm for diagram shrinking.
    Implements ShrinkingAlgorithm interface.
    """

    def __init__(self):
        self.weights_map = None
        self.PUML = None
        self.size = None
        self.edges = None
        self.vertex_data = None
        self.class_to_index = {}

    def compute(self, parsed_puml: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run Kruskal's algorithm on parsed PUML data and return the MST.

        Args:
            parsed_puml: Dictionary with 'classes' and 'edges' keys

        Returns:
            Reduced PUML dictionary with MST edges
        """
        self.PUML = parsed_puml
        self.size = len(parsed_puml["classes"])
        self.edges = []
        self.vertex_data = [""] * self.size
        self.class_to_index = {
            class_name: index
            for index, class_name in enumerate(parsed_puml["classes"].keys())
        }

        self.extract_puml_data(parsed_puml)
        return self.solve()

    def get_weight(self, association_type):
        """Get weight for given association type from config."""
        if association_type in self.weights_map:
            return self.weights_map[association_type]

        association_lower = association_type.lower().strip()
        for key, value in self.weights_map.items():
            if key.lower().strip() == association_lower:
                return value

        return 1

    def extract_puml_data(self, PUML):
        for class_name, index in self.class_to_index.items():
            self.add_vertex_data(index, class_name)

        for edge in PUML["edges"]:
            source = edge["source"]
            target = edge["target"]

            relation = edge.get("relation", "association")
            association_type = relation.lower().strip().split("-")[0]
            weight = self.get_weight(association_type)

            if source in self.class_to_index and target in self.class_to_index:
                u = self.class_to_index[source]
                v = self.class_to_index[target]
                self.add_edge(u, v, weight)

    def add_edge(self, u, v, weight):
        if 0 <= u < self.size and 0 <= v < self.size:
            self.edges.append((u, v, weight))  # Add edge with weight

    def add_vertex_data(self, vertex, data):
        if 0 <= vertex < self.size:
            self.vertex_data[vertex] = data

    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    def union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    def solve(self):
        result = []  # MST
        i = 0  # edge counter

        self.edges = sorted(self.edges, key=lambda item: item[2])

        parent, rank = [], []

        for node in range(self.size):
            parent.append(node)
            rank.append(0)

        while i < len(self.edges):
            u, v, weight = self.edges[i]
            i += 1
            x = self.find(parent, u)
            y = self.find(parent, v)
            if x != y:
                result.append((u, v, weight))
                self.union(parent, rank, x, y)

        return self.extract_solution(result)

    def extract_solution(self, sol):
        assert self.PUML is not None, "PUML data not initialized"
        edges = []
        edge_lookup = {}

        for edge in self.PUML["edges"]:
            source = edge["source"]
            target = edge["target"]
            if source not in self.class_to_index or target not in self.class_to_index:
                continue
            u = self.class_to_index[source]
            v = self.class_to_index[target]
            edge_lookup[(u, v)] = edge
            edge_lookup[(v, u)] = edge

        for u, v, weight in sol:
            original_edge = edge_lookup.get((u, v), edge_lookup.get((v, u)))
            if original_edge:
                edges.append(original_edge)

        return {"classes": self.PUML["classes"], "edges": edges}
