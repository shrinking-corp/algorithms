from shrinking_algorithms import DiagramShrinker

class KruskalDiagramShrinker(DiagramShrinker):
    def __init__(self, config: dict = None, **params):
        super().__init__(algorithm="kruskals", config=config, **params)