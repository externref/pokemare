import json

from disnake.flags import Intents
from disnake.activity import Activity
from disnake.enums import ActivityType, Status
from disnake.ext.commands.bot import Bot, when_mentioned_or

from .database import UserInfoDatabase


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
        self.color = 0x04356D
        self.load_extension("jishaku")
        self.get_cog("Jishaku").hidden = True
        self.load_extension("pokemare.cogs.start")
        self.load_extension("pokemare.cogs.tools")
        self.load_extension("pokemare.cogs.general")
        self.load_extension("pokemare.cogs.miscs")
        self.load_extension("pokemare.cogs.help")
        self.support_server_invite_url = "https://discord.gg/Km8WwHBSrg"
        with open("data/pokemons.json", "r") as file:
            self.pokemon_dict = json.load(file)

    async def on_ready(self):
        self.user_database = UserInfoDatabase("users.db", self)
        await self.user_database.create_and_connect()
        self.invite_url = f"https://discordapp.com/oauth2/authorize?client_id={self.user.id}&scope=bot+applications.commands&permissions=3691367512"
        print("Bot Online", self.latency * 1000)

    def run(self):
        super().run(self.token)


if __name__ == "__main__":
    PokeMare = PokeMare()
