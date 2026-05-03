from shrinking_algorithms import DiagramShrinker
from shrinking_algorithms.shrinkers import KruskalDiagramShrinker

import os
import json
import unittest

class TestKruskalAlgorithm(unittest.TestCase):

    def test_kruskal_file1(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        puml_file_path = os.path.join(current_dir, "puml_files", "file1.puml")

        with open(puml_file_path, "r", encoding="utf-8") as file:
            content = file.read()

        algorithm = KruskalDiagramShrinker(content)
        result = algorithm.shrink().get_all()

        self.assertIsNotNone(result)

        puml_file_result_path = os.path.join(current_dir, "puml_files", "file1_kruskal.json")
        file_sample = open(file=puml_file_result_path, encoding="UTF-8")

        reader = file_sample.read()
        file_sample.close()
        json_sample = json.loads(reader)

        self.assertEqual(result, json_sample)

    def test_kruskal_file2(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        puml_file_path = os.path.join(current_dir, "puml_files", "file2.puml")

        with open(puml_file_path, "r", encoding="utf-8") as file:
            content = file.read()

        algorithm = DiagramShrinker(content)
        result = algorithm.shrink().get_all()

        self.assertIsNotNone(result)

        puml_file_result_path = os.path.join(current_dir, "puml_files", "file2_kruskal.json")
        file_sample = open(file=puml_file_result_path, encoding="UTF-8")

        reader = file_sample.read()
        file_sample.close()
        json_sample = json.loads(reader)

        self.assertEqual(result, json_sample)

    def test_kruskal_file3(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        puml_file_path = os.path.join(current_dir, "puml_files", "file3.puml")

        with open(puml_file_path, "r", encoding="utf-8") as file:
            content = file.read()

        algorithm = DiagramShrinker(
            puml_content=content,
            algorithm="kruskals"
        )
        result = algorithm.shrink().get_all()

        self.assertIsNotNone(result)

        puml_file_result_path = os.path.join(current_dir, "puml_files", "file3_kruskal.json")
        file_sample = open(file=puml_file_result_path, encoding="UTF-8")

        reader = file_sample.read()
        file_sample.close()
        json_sample = json.loads(reader)

        self.assertEqual(result, json_sample)