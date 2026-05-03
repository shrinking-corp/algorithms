from shrinking_algorithms import DiagramShrinker
from shrinking_algorithms.shrinkers import EvolDiagramShrinker

import os
import unittest

class TestGenericAlgorithm(unittest.TestCase):

    def test_evolution_file1(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        puml_file_path = os.path.join(current_dir, "puml_files", "file1.puml")

        with open(puml_file_path, "r", encoding="utf-8") as file:
            content = file.read()

        config = {"iterations": 6}
        algorithm = EvolDiagramShrinker(
            puml_content=content,
            config=config
        )
        result = algorithm.shrink().get_all()

        self.assertIsNotNone(result)

    def test_evolution_file2(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        puml_file_path = os.path.join(current_dir, "puml_files", "file2.puml")

        with open(puml_file_path, "r", encoding="utf-8") as file:
            content = file.read()

        algorithm = DiagramShrinker(
            puml_content=content,
            algorithm="evol",
            iterations=5
        )
        result = algorithm.shrink().get_all()

        self.assertIsNotNone(result)

    def test_evolution_file3(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        puml_file_path = os.path.join(current_dir, "puml_files", "file3.puml")

        with open(puml_file_path, "r", encoding="utf-8") as file:
            content = file.read()

        algorithm = DiagramShrinker(
            puml_content=content,
            algorithm="evol",
            iterations=5
        )
        result = algorithm.shrink().get_all()

        self.assertIsNotNone(result)

    def test_evolution_file4(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        puml_file_path = os.path.join(current_dir, "puml_files", "file4.puml")

        with open(puml_file_path, "r", encoding="utf-8") as file:
            content = file.read()

        algorithm = DiagramShrinker(
            puml_content=content,
            algorithm="evol",
            iterations=5
        )
        result = algorithm.shrink().get_all()

        self.assertIsNotNone(result)