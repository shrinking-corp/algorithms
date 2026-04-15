import networkx as nx
import numpy as np
import os
import json
from pathlib import Path


WEIGHTS_FILE = os.path.join(Path(__file__).parent, "weights.json")

with open(WEIGHTS_FILE, "r") as f:
    WEIGHTS = json.load(f)

assert WEIGHTS is not None, "Embedding weights file not found"


def uml_dict_to_graph(uml: dict) -> tuple[nx.DiGraph, dict]:
    """
    Converts a UML representation provided as a dictionary into a directed graph
    using `networkx.DiGraph`. The graph captures the relationships, attributes,
    and structure defined within the UML dictionary.

    :param uml: Dictionary representing the UML structure. It should contain
        the following keys:
        - "classes": A dictionary where keys are class names and values contain
          attributes for each class (e.g., "attributes", "methods").
        - "edges": A list of dictionaries, each representing a relationship
          between classes (e.g., "source", "target", "relation").
    :type uml: dict
    :return: A directed graph where nodes represent classes with associated
        metadata attributes and edges represent class relationships based on
        the provided UML.
    :rtype: nx.DiGraph
    """
    class_class_edges = 0
    class_attr_edges = 0
    class_method_edges = 0

    G = nx.DiGraph()
    classes = list(uml.get("classes", {}).keys())

    connector_enabled = WEIGHTS["weights"]["connector"]["enabled"]
    connector = "__node_connector__"
    c_w = WEIGHTS["weights"]["connector"]["weight"]

    if connector_enabled:
        G.add_node(connector)

    for cls_name in classes:
        # print(uml["classes"][cls_name])
        G.add_node(cls_name)

        if connector_enabled:
            G.add_edge(connector, cls_name, weight=c_w)
            penalize_node2connector = 0.5
            G.add_edge(
                cls_name, connector, weight=c_w * penalize_node2connector
            )  # make sure walks do not pick connector often

        for attr in uml["classes"][cls_name].get("attributes", []):
            attr_uuid = f"{cls_name}::attr::{attr['name']}"
            # print(attr_uuid)
            G.add_node(attr_uuid)
            w1 = WEIGHTS["weights"]["attribute_edges"]["class_to_attribute"]
            G.add_edge(cls_name, attr_uuid, weight=w1)
            w2 = WEIGHTS["weights"]["attribute_edges"]["attribute_to_class"]
            G.add_edge(attr_uuid, cls_name, weight=w2)

            class_attr_edges += 1

        for method in uml["classes"][cls_name].get("methods", []):
            method_uuid = f"{cls_name}::method::{method['name']}::{method['signature']}"
            # print(method_uuid)
            G.add_node(method_uuid)
            w1 = WEIGHTS["weights"]["method_edges"]["class_to_method"]
            G.add_edge(cls_name, method_uuid, weight=w1)
            w2 = WEIGHTS["weights"]["method_edges"]["method_to_class"]
            G.add_edge(method_uuid, cls_name, weight=w2)

            class_method_edges += 1

        # print()

    for edge in uml.get("edges", []):
        src = edge["source"]
        dst = edge["target"]
        rel = edge["relation"]

        if src not in G or dst not in G:
            continue

        class_class_edges += 1

        if "-" in rel:
            rel, direction = rel.split("-")
            if direction == "right":
                w1 = WEIGHTS["weights"]["class_edges"][rel]["forward"]
                G.add_edge(src, dst, weight=w1)
                w2 = WEIGHTS["weights"]["class_edges"][rel]["reverse"]
                G.add_edge(dst, src, weight=w2)
            else:
                w1 = WEIGHTS["weights"]["class_edges"][rel]["forward"]
                G.add_edge(dst, src, weight=w1)
                w2 = WEIGHTS["weights"]["class_edges"][rel]["reverse"]
                G.add_edge(src, dst, weight=w2)
        else:
            w = WEIGHTS["weights"]["class_edges"][rel]["forward"]
            G.add_edge(src, dst, weight=w)
            G.add_edge(dst, src, weight=w)

    stats = {
        "total_edges": class_class_edges + class_attr_edges + class_method_edges,
        "class_class_edges": class_class_edges,
        "class_attr_edges": class_attr_edges,
        "class_method_edges": class_method_edges,
    }

    return G, stats


def normalized_degree_histogram(G, bins=5):
    degrees = [d for _, d in G.degree()]
    if not degrees:
        return np.zeros(bins)

    hist, _ = np.histogram(degrees, bins=bins, range=(0, max(degrees)))
    hist = hist.astype(float)
    return hist / hist.sum()


def cycle_ratio(G):
    if G.number_of_edges() == 0:
        return 0.0

    try:
        cycles = nx.simple_cycles(G) if G.is_directed() else nx.cycle_basis(G)
        num_cycles = len(list(cycles))
    except Exception:
        num_cycles = 0

    return min(1.0, num_cycles / G.number_of_edges())


def hierarchy_depth(G):
    if G.number_of_nodes() == 0:
        return 0.0

    if not G.is_directed():
        return 0.0

    scc_graph = nx.condensation(G)

    if not nx.is_directed_acyclic_graph(scc_graph):
        return 0.0

    depth = nx.dag_longest_path_length(scc_graph)
    return depth / max(1, G.number_of_nodes())


def scc_size_histogram(G, bins=5):
    if not G.is_directed():
        return np.zeros(bins)

    sccs = list(nx.strongly_connected_components(G))
    sizes = [len(scc) for scc in sccs]

    if not sizes:
        return np.zeros(bins)

    hist, _ = np.histogram(sizes, bins=bins, range=(1, max(sizes)))
    hist = hist.astype(float)
    return hist / hist.sum()


def centrality_rank_vector(G, k=5):
    if G.number_of_nodes() == 0:
        return np.zeros(k)

    centrality = nx.betweenness_centrality(G, normalized=True)
    ranked = sorted(centrality.values(), reverse=True)

    ranked = ranked[:k]
    if len(ranked) < k:
        ranked += [0.0] * (k - len(ranked))

    ranked = np.array(ranked)
    if ranked.sum() == 0:
        return ranked

    return ranked / ranked.sum()
