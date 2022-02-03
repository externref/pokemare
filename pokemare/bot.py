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
        self.get_cog('Jishaku').hidden = True
        self.load_extension("pokemare.cogs.start")
        self.load_extension("pokemare.cogs.tools")
        self.load_extension("pokemare.cogs.help")
        self.invite_url = "https://discordapp.com/oauth2/authorize?client_id=936957153225363496&scope=bot+applications.commands&permissions=3691367512"
        self.support_server_invite_url = 'https://discord.gg/Km8WwHBSrg'
    def run(self):
        super().run(self.token)


if __name__ == "__main__":
    PokeMare = PokeMare()
