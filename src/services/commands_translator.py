from discord import app_commands, Locale
from pathlib import Path

from ..utils import load_json_file

CMD_LOCALES_DIR = "data/locales/commands"


class CommandsTranslator(app_commands.Translator):
    """A class that handles translations for commands, parameters, and choices.

    Translations are done lazily in order to allow for async enabled translations as well
    as supporting a wide array of translation systems such as :mod:`gettext` and
    `Project Fluent <https://projectfluent.org>`_.

    In order for a translator to be used, it must be set using the :meth:`CommandTree.set_translator`
    method. The translation flow for a string is as follows:

    1. Use :class:`locale_str` instead of :class:`str` in areas of a command you want to be translated.
        - Currently, these are command names, command descriptions, parameter names, parameter descriptions, and choice names.
        - This can also be used inside the :func:`~discord.app_commands.describe` decorator.
    2. Call :meth:`CommandTree.set_translator` to the translator instance that will handle the translations.
    3. Call :meth:`CommandTree.sync`
    4. The library will call :meth:`Translator.translate` on all the relevant strings being translated.

    .. versionadded:: 2.0
    """
    default_locale: Locale = Locale.american_english
    translations: dict[Locale, dict[str, str]] = {Locale.american_english:{}}

    async def load(self) -> None:
        """|coro|

        An asynchronous setup function for loading the translation system.

        The default implementation does nothing.

        This is invoked when :meth:`CommandTree.set_translator` is called.
        """

        translations_dir = Path(__file__).resolve().parent.parent.parent / CMD_LOCALES_DIR

        if not translations_dir.exists():
            raise FileNotFoundError("Unable to find the folder containing the command translations")

        translations_files = [file.name[:-5] for file in translations_dir.glob('*.json')]

        if len(translations_files) == 0 or "en-US" not in translations_files:
            raise FileNotFoundError(f"Unable to locate the en-US.json file in the '{CMD_LOCALES_DIR}' folder")

        for locale in Locale:
            if locale.value in translations_files:
                self.translations[locale] = load_json_file(translations_dir/f"{locale.value}.json")

    async def translate(self, string: app_commands.locale_str, locale: Locale, context: app_commands.TranslationContext) -> str | None:
        """|coro|

        Translates the given string to the specified locale.

        If the string cannot be translated, ``None`` should be returned.

        The default implementation returns ``None``.

        If an exception is raised in this method, it should inherit from :exc:`TranslationError`.
        If it doesn't, then when this is called the exception will be chained with it instead.

        Parameters
        ------------
        string: :class:`locale_str`
            The string being translated.
        locale: :class:`~discord.Locale`
            The locale being requested for translation.
        context: :class:`TranslationContext`
            The translation context where the string originated from.
            For better type checking ergonomics, the ``TranslationContextTypes``
            type can be used instead to aid with type narrowing. It is functionally
            equivalent to :class:`TranslationContext`.
        """

        if locale not in self.translations or locale is None:
            locale = self.default_locale

        if string.message in self.translations[locale]:
            return self.translations[locale][string.message]

        # Return default locale if not value finded for the locale given.
        if string.message in self.translations[self.default_locale]:
            return self.translations[self.default_locale][string.message]

        return None