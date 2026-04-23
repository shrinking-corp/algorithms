from shrinking_algorithms import DiagramShrinker

from typing import Optional

class KruskalDiagramShrinker(DiagramShrinker):

    def __init__(self,
                 puml_content: Optional[str] = None,
                 config: Optional[dict] = None,
                 **params):
        super().__init__(
            puml_content=puml_content,
            algorithm="kruskals",
            config=config,
            **params
        )