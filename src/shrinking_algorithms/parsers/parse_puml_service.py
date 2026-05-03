from typing import Optional, Any
import json
import re

class PUMLParser:
    def __init__(self, config_path="parser_config.json"):
        self.relations = {}
        self.class_names = set()
        self.parse_config(config_path)

        if not self.relations:
            print("No relations loaded, using default settings.")
            return

    def parse_config(self, config_path):
        if config_path is None:
            print("No config path provided, loading default config.")
            return {}

        try:
            with open(config_path, "r") as file:
                config = json.load(file)
                self.relations = config.get("relations", {})
                self.class_names = set(config.get("class_names", []))
                return config

        except Exception as e:
            print(f"Error reading config file: {e}")
            return {}

    def parse_file(self, content: str) -> dict:
        if not self.is_correct_puml(content):
            raise TypeError("Provided content is not a correct PUML format.")
        lines = self.remove_comments(content)

        classes = {}
        classes_count = 0
        edges = []
        current_class = None
        in_class_body = False

        for i, line in enumerate(lines):
            line = line.strip()
            is_class_declaration = False

            for keyword in self.class_names:
                if line.startswith(keyword):
                    class_name = self.extract_class_name(keyword, line)
                    if class_name:
                        current_class = class_name
                        classes[class_name] = {
                            "id": classes_count,
                            "attributes": [],
                            "methods": []
                        }
                        classes_count += 1
                        in_class_body = line.endswith("{")
                        is_class_declaration = True
                    break

            if in_class_body and line == "}":
                in_class_body = False
                current_class = None
                continue

            if in_class_body and current_class and not is_class_declaration:
                member = self.parse_class_member(line)
                if member:
                    if member["type"] == "attribute":
                        classes[current_class]["attributes"].append({
                            "name": member["name"],
                            "visibility": member["visibility"],
                            "datatype": member.get("datatype", "")
                        })
                    elif member["type"] == "method":
                        classes[current_class]["methods"].append({
                            "name": member["name"],
                            "visibility": member["visibility"],
                            "signature": member["signature"]
                        })

            for relation_key, relation_value in self.relations.items():
                line_without_brackets = re.sub(r'\[.*?\]', '', line.strip())
                if relation_key in line_without_brackets:
                    parts = line_without_brackets.split(relation_key)
                    edge = self.extract_edge_info(parts)

                    source = edge.get("source")
                    target = edge.get("target")
                    if source in classes and target in classes:
                        edges.append(edge | {"relation": relation_value})
                    break

        return {"classes": classes, "edges": edges}

    def reparse_file(self, content: str, new_data: dict) -> list[str]:

        if not content:
            raise TypeError("Original puml content for reparsing is empty.")

        if not new_data:
            raise TypeError("No new data provided for reparsing.")

        original_lines = content.strip().split("\n")
        lines = []
        current_class = None
        in_class_body = False
        skip_class = False

        for line in original_lines:
            append_line = True
            stripped_line = line.strip()
            is_class_declaration = False

            for keyword in self.class_names:
                if stripped_line.startswith(keyword):
                    class_name = self.extract_class_name(keyword, stripped_line)
                    if class_name:
                        current_class = class_name
                        is_class_declaration = True
                        if class_name not in new_data.get("classes", {}):
                            skip_class = True
                            append_line = False
                        else:
                            skip_class = False
                            in_class_body = stripped_line.endswith("{")
                    break

            if in_class_body and stripped_line == "}":
                in_class_body = False
                if skip_class:
                    append_line = False
                current_class = None
                skip_class = False

            elif skip_class:
                append_line = False

            elif in_class_body and current_class and current_class in new_data.get("classes", {}) and not is_class_declaration:
                member = self.parse_class_member(stripped_line)
                if member:
                    class_data = new_data["classes"][current_class]

                    if member["type"] == "attribute":
                        attr_exists = any(
                            attr["name"] == member["name"] and
                            attr["visibility"] == member["visibility"]
                            for attr in class_data.get("attributes", [])
                        )
                        if not attr_exists:
                            append_line = False

                    elif member["type"] == "method":
                        method_exists = any(
                            method["signature"] == member["signature"] and
                            method["visibility"] == member["visibility"]
                            for method in class_data.get("methods", [])
                        )
                        if not method_exists:
                            append_line = False

            if not is_class_declaration:
                for relation_key, relation_value in self.relations.items():
                    line_without_brackets = re.sub(r'\[.*?\]', '', stripped_line)
                    if relation_key in line_without_brackets:
                        lineWithoutComments = re.sub(r"/\'.*?'\/", "", line_without_brackets, flags=re.DOTALL).strip()
                        parts = lineWithoutComments.split(relation_key)
                        edge = self.extract_edge_info(parts)

                        source = edge.get("source")
                        target = edge.get("target")

                        # Check if this edge exists in new_data
                        edge_exists = False
                        for new_edge in new_data.get("edges", []):
                            if (new_edge.get("source") == source and
                                new_edge.get("target") == target and
                                new_edge.get("relation") == relation_value):
                                edge_exists = True
                                break

                        if not edge_exists:
                            append_line = False
                        elif source not in new_data.get("classes", {}) or target not in new_data.get("classes", {}):
                            append_line = False
                        break

            if append_line:
                lines.append(line)

        return lines

    @staticmethod
    def is_correct_puml(content: str) -> bool:
        lines = content.strip().split("\n")
        start_found = False
        end_found = False

        for line in lines:
            line = line.strip()
            if line == "@startuml":
                start_found = True
            elif line == "@enduml":
                end_found = True

        return start_found and end_found

    @staticmethod
    def remove_comments(content: str) -> list[str]:
        content = re.sub(r"/\'.*?\'\/", "", content, flags=re.DOTALL)
        return content.strip().split("\n")

    @staticmethod
    def extract_class_name(keyword: str, line: str) -> str:
        name = line.replace(keyword + " ", "").split(" ")[0].strip()
        if name:
            return name
        return ""

    @staticmethod
    def extract_edge_info(parts: list[str]) -> dict[str, str]:
        if len(parts) == 2:
            source = parts[0]
            target = parts[1]

            if ':' in target:
                target = target.split(':')[0].strip()

            if '"' in source:
                source = source.split('"')[0].strip()

            if '"' in target:
                target = target.split('"')[-1].strip()

            return {"source": source, "target": target}
        return {}

    @staticmethod
    def parse_class_member(line: str) -> Optional[dict[str, Any]]:
        """Parse a class member (attribute or method) with visibility modifier."""
        line = line.strip()
        if not line or line.startswith("//") or line.startswith("'"):
            return None

        visibility_map = {"+": "public", "-": "private", "#": "protected", "~": "package"}
        visibility = "public"
        
        if line and line[0] in visibility_map:
            visibility = visibility_map[line[0]]
            line = line[1:].strip()

        if "(" in line and ")" in line:
            method_match = re.match(r'([a-zA-Z_]\w*)\s*\((.*?)\)', line)
            if method_match:
                method_name = method_match.group(1)
                params = method_match.group(2).strip()
                signature = f"{method_name}({params})"
                return {
                    "type": "method",
                    "name": method_name,
                    "visibility": visibility,
                    "signature": signature
                }
        
        else:
            attr_match = re.match(r'([a-zA-Z_]\w*)\s*(?::\s*(.+))?', line)
            if attr_match:
                attr_name = attr_match.group(1)
                datatype = attr_match.group(2).strip() if attr_match.group(2) else ""
                return {
                    "type": "attribute",
                    "name": attr_name,
                    "visibility": visibility,
                    "datatype": datatype
                }

        return None
