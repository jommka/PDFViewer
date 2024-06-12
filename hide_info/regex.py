import json


class Regex:

    def __init__(self):
        self.pattern = self.read_json()

    @staticmethod
    def read_json():
        with open('hide_info/json/regex.json', 'r', encoding='utf-8') as f:
            text = json.load(f)
        return text

    def get_pattern(self):
        return self.pattern

