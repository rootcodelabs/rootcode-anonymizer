# -*- coding: utf-8 -*-
import json
import re

class RegexStringProcessor:
    def __init__(self):
        pass

    def load_regex_patterns(self, json_file_path):
        with open(json_file_path, 'r') as file:
            regex_data = json.load(file)
        return regex_data.get("patterns", [])

    def apply_regex_substitution(self, input_string):
        self.regex_patterns = self.load_regex_patterns("regex_patterns.json")
        for pattern_data in self.regex_patterns:
            pattern = pattern_data["pattern"]
            replacement = pattern_data["replacement"]
            input_string = re.sub(pattern, replacement, input_string)
        return input_string