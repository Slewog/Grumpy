from discord import Intents

def build_intents() -> Intents:
    intents = Intents.default()
    intents.message_content = True
    intents.members = True
    intents.reactions = True
    intents.guilds = True

    return intents