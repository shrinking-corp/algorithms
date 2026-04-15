from shrinking_algorithms import DiagramShrinker

class EvolDiagramShrinker(DiagramShrinker):
    def __init__(self, config: dict = None, **params):
        super().__init__(algorithm="evol", config=config, **params)