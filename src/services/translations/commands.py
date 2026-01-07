from discord import app_commands, Locale

class CommandsTranslator(app_commands.Translator):
    translations: dict[Locale, dict[str, str]] = {}

    async def load(self) -> None:
        """|coro|

        An asynchronous setup function for loading the translation system.

        The default implementation does nothing.

        This is invoked when :meth:`CommandTree.set_translator` is called.
        """
        self.translations = {
            Locale.french: {
                "Purge a text channel": "Purger un salon de text"
            }
        }
    async def translate(self, string: app_commands.locale_str, locale: Locale, context: app_commands.TranslationContext) -> str | None:
        """
            This method is called for each string to be translated

            Args:
                locale_str: The string to translate (contains the key)
                locale: The target language (ex: discord.Locale.french)
                context: The context (commande, paramètre, choix, etc.)

            Returns:
                The translation or None to use the default value
        """

        if locale in self.translations and string.message in self.translations[locale]:
            return self.translations[locale][string.message]

        return None