from shrinking_algorithms.parsers import PUMLParser
from shrinking_algorithms.algorithms import AlgorithmType, Factory
from shrinking_algorithms.algorithms.preprocessing.preprocess_step_factory import PreprocessStepFactory
from shrinking_algorithms.algorithms.preprocessing.preprocess_decorator import PreprocessingDecorator

import os
import tempfile

def process_puml(content: str, algorithm_type: AlgorithmType, settings: dict):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, "parsers", "parser_config.json")
    parser = PUMLParser(config_path)

    source_path = None
    output_path = None

    print(algorithm_type)
    print(settings)

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".puml") as tmp:
            tmp.write(content.encode("utf-8"))
            source_path = tmp.name

        parsed = parser.parse_file(
            source_path
        )
        if not parsed:
            raise TypeError("Unable to parse PUML file")

        creator = Factory.get_creator(algorithm_type)
        algorithm = creator.get_algorithm(settings)
        if settings and settings.get("preprocess_steps"):
            steps = settings["preprocess_steps"]
            pp_factory = PreprocessStepFactory()
            steps = [pp_factory.get_step(step) for step in steps]
            algorithm = PreprocessingDecorator(algorithm, steps)

        reduced = algorithm.compute(parsed)

        with tempfile.NamedTemporaryFile(
            delete=False, suffix="_reduced.puml"
        ) as tmp_out:
            output_path = tmp_out.name
        parser.reparse_file(source_path, output_path, reduced)
        with open(output_path, "r", encoding="utf-8") as f:
            result = f.read()

        return {"parsed": parsed, "reduced": reduced, "result_puml": result}

    except Exception as e:
        raise RuntimeError(e.__str__())

    finally:
        if source_path and os.path.exists(source_path):
            try:
                os.remove(source_path)
            except:
                pass
        if output_path and os.path.exists(output_path):
            try:
                os.remove(output_path)
            except:
                pass
