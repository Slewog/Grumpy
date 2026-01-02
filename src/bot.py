from dataclasses import dataclass

from discord.ext import commands

from src.configs import Settings, get_settings, build_intents

@dataclass(slots=True)
class GrumpyApp:
    settings: Settings
    bot: commands.Bot

    def run(self) -> None:
        self.bot.run(self.settings.token)


class Grumpy(commands.Bot):
    def __init__(self, *, settings: Settings) -> None:
        intents = build_intents()
        super().__init__(
            command_prefix=settings.command_prefix,
            intents=intents,
            # description="Grumpy Discord Bot",
        )

    async def setup_hook(self) -> None:
        """Load cogs and perform setup tasks here."""
        print("Setting up bot...")
        # Load cogs here

    async def on_ready(self) -> None:
        """Called when the bot is ready."""
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        # Set commands translation here
        # Sync commands here

def create_app() -> GrumpyApp:
    settings = get_settings()

    bot = Grumpy(settings=settings)
    return GrumpyApp(settings=settings, bot=bot)