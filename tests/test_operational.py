from app import process_puml
import unittest

class TestKruskalAlgorithm(unittest.TestCase):

    def test_kruskal_file(self):
        file = open(file="puml_files/file1.puml", encoding="UTF-8")

        kruskals_settings = ('{'
            '"weights": {'
                '"dependency": 1,'
                '"extension" : 3,'
                '"implementation" : 3,'
                'aggregation" : 2,'
                'composition" : 2,'
                '"association" : 1'
            '}'
        '}')

        result = process_puml(
            file=file,
            algorithm="kruskals",
            settings='{}'
        )

        self.assertIsNotNone(result)

class TestGenericAlgorithm(unittest.TestCase):

    def test_generic_operational(self):
        file = open(file="puml_files/file1.puml", encoding="UTF-8")

        result = process_puml(
            file=file,
            algorithm="evol",
            settings='{"iterations": 5}'
        )

        self.assertIsNotNone(result)