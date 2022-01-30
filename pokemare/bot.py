from disnake.ext.commands.bot import Bot, when_mentioned_or
from disnake.flags import Intents
from disnake.activity import Activity
from disnake.enums import ActivityType, Status


class PokeMare(Bot):
    def __init__(self, token):
        super().__init__(
            command_prefix=when_mentioned_or("."),
            intents=Intents.all(),
            case_insensitive=True,
            strip_after_prefix=True,
            activity=Activity(type=ActivityType.listening, name=".help"),
            status=Status.dnd,
        )
        self.token = token
        self.load_extension("jishaku")
        self.load_extension("pokemare.cogs.start")

    def run(self):
        super().run(self.token)


if __name__ == "__main__":
    PokeMare = PokeMare()
