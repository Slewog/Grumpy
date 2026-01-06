import json
from pathlib import Path
from discord import app_commands, Locale


class TextTranslator:
    def __init__(self, locales_path: Path, default_locale: str ='en'):
        self.default_locale = default_locale
        self.translations = {}

    def load_translations(self, locales_path: Path):
        pass

    def get(self, key: str, locale: Locale = None, **kwargs):
        pass