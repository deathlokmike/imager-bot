import json


class Translator:
    _instances: dict[str, 'Translator'] = {}

    def __new__(cls, locale: str) -> 'Translator':
        if locale not in cls._instances:
            cls._instances[locale] = super(Translator, cls).__new__(cls)
        return cls._instances[locale]

    def __init__(self, locale: str):
        self.locale = locale

    def get_translate(self, command: str, dataclass_):
        with open(f"imager_bot/locales/{self.locale}/{command}.json", encoding="utf-8") as file:
            translation = json.load(file)

        return dataclass_(**translation)
