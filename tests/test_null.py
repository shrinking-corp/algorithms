from shrinking_algorithms import DiagramShrinker
from shrinking_algorithms.algorithms.creators import NullCreator

import os
import unittest

class TestNullAlgorithm(unittest.TestCase):

    def test_singleton(self):
        algorithm1 = NullCreator.get_algorithm()
        algorithm2 = NullCreator.get_algorithm()
        self.assertEqual(algorithm1, algorithm2)

    def test_null_algorithm_file1(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        puml_file_path = os.path.join(current_dir, "puml_files", "file1.puml")

        with open(puml_file_path, "r", encoding="utf-8") as file:
            content = file.read()

        algorithm = DiagramShrinker(content, algorithm="null")
        result = algorithm.shrink().get_result_puml()

        self.assertIsNotNone(result)
        self.assertEqual(result, content)

    def test_null_algorithm_file2(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        puml_file_path = os.path.join(current_dir, "puml_files", "file2.puml")

        with open(puml_file_path, "r", encoding="utf-8") as file:
            content = file.read()

        algorithm = DiagramShrinker(content, algorithm="null")
        result = algorithm.shrink().get_result_puml()

        self.assertIsNotNone(result)
        self.assertEqual(result, content)

    def test_null_algorithm_file3(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        puml_file_path = os.path.join(current_dir, "puml_files", "file3.puml")

        with open(puml_file_path, "r", encoding="utf-8") as file:
            content = file.read()

        algorithm = DiagramShrinker(content, algorithm="null")
        result = algorithm.shrink().get_result_puml()

        self.assertIsNotNone(result)
        self.assertEqual(result, content)