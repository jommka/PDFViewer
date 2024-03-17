import json


class Regex:

    def __init__(self):
        self.pattern = self.read_json()

    @staticmethod
    def read_json():
        with open('./json/regex.json', 'r', encoding='utf-8') as f:
            text = json.load(f)
        return text

    def get_pattern(self):
        return self.pattern

    # "passport_issued_by": "[В|в]ыдан[а-яё]*\\s+([А-ЯЁ]+\\s{0,3})*(«*[А-ЯЁ]*[а-яё]+»*\\s{0,3})*([г.][А-ЯЁ][
    # а-яё]+\\s{0,3}([А-ЯЁ]*[а-яё]+\\s{0,3})*)*", "SNILS": "(\\d{3}\\s*-*\\s*\\d{3}\\s*-*\\s*\\d{3}\\s*-*\\s*\\d{
    # 2})", "INN": "ИНН\\s*(\\d\\s*){10,15}",
