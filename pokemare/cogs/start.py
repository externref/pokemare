import aiosqlite
from aiohttp import ClientSession
from disnake.ext.commands.bot import Bot
from disnake.ext.commands.cog import Cog
from disnake.ext.commands.core import command
from disnake.ext.commands.context import Context
from disnake.ui import View, Button, button
from disnake.enums import ButtonStyle
from disnake.interactions import MessageInteraction
from disnake.embeds import Embed
from disnake.file import File
from disnake.colour import Color


desc = """
<:moonball:918870698997452831> Welcome to the world of **PokéMare**, and the start of your Pokémon Journey!
Register your trainer account, by picking one of these three starter Pokémon!

<:Bulbasaur:936975459688779776> : **Bulbasaur** | <:Charmander:936975190468997120> : **Charmander** | <:squirtle:937042783804473384> : **Squirtle**
"""


class Start(Cog, name="Startup Command"):
    """Start with your PokéMare journey !"""

    def __init__(self, bot: Bot) -> None:
        self.hidden = False
        self.emoji = "<:trainer:937618424169914398>"
        self.bot = bot

    @Cog.listener("on_ready")
    async def connect_to_database(self):
        self.bot.user_database = await aiosqlite.connect("users.db")
        async with self.bot.user_database.cursor() as cursor:
            await cursor.execute(
                """CREATE TABLE IF NOT EXISTS starters (user_id TEXT , pokemon TEXT)"""
            )
            await self.bot.user_database.commit()

    async def check_if_in_database(self, ctx: Context):
        async with self.bot.user_database.cursor() as cursor:
            await cursor.execute(
                """SELECT * FROM starters WHERE user_id = ?""",
                (str(ctx.author.id),),
            )

            data = await cursor.fetchone()
        if data:
            return True

    @command(name="start", description="Begin your pokemon journey!")
    async def start(self, ctx: Context):
        has_account = await self.check_if_in_database(ctx)
        if has_account:
            return await ctx.reply("You already have  pokemon")
        embed = Embed(color=0xFFFFFF, description=desc, title="Professor Oak")
        embed.set_image(
            "https://media.discordapp.net/attachments/937603105443442769/937603206534549514/choose_pokemon.png"
        )
        embed.set_footer(text="You have 30 seconds to respond")
        my_view = SelectPokemon(ctx.bot)
        my_view.message = await ctx.send(embed=embed, view=my_view)


def setup(bot: Bot):
    bot.add_cog(Start(bot))


class SelectPokemon(View):
    def __init__(self, bot):
        self.bot: Bot = bot
        super().__init__(timeout=30)

    async def insert_into_database(self, user_id: int, pokemon: str):
        await self.message.edit(
            view=None,
            embed=Embed(
                color=0xFFFFFF,
                description=f"Oh? **{pokemon.title()}**, a fine choice! Confirm your pick by typing in `I agree`! ",
            ),
            files=[],
        )
        try:
            await self.bot.wait_for(
                "message",
                check=lambda m: m.author.id == user_id
                and m.content.lower() == "i agree",
                timeout=30,
            )
        except:
            return await self.message.channel.send(
                f"<@!{user_id}> you didn't respond with `I Agree`"
            )
        async with self.bot.user_database.cursor() as cursor:
            await cursor.execute(
                """INSERT INTO starters (user_id ,pokemon) VALUES (? , ?)""",
                (str(user_id), pokemon),
            )
        await self.bot.user_database.commit()
        return True

    async def disable(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)

    @button(emoji="<:Bulbasaur:936975459688779776>", style=ButtonStyle.green)
    async def bulbasaur(self, button: Button, interaction: MessageInteraction):
        await interaction.response.defer()
        a = await self.insert_into_database(interaction.author.id, "bulbasaur")
        if not a:
            return
        await self.message.edit(
            embed=Embed(
                color=0xFFFFFF,
                description="You picked Bulbasaur\nUse `.dex bulbasaur` to get more info about it!",
            ),
            view=None,
            files=[],
        )

    @button(emoji="<:Charmander:936975190468997120>", style=ButtonStyle.red)
    async def charmander(self, button: Button, interaction: MessageInteraction):
        await interaction.response.defer()
        a = await self.insert_into_database(interaction.author.id, "charmander")
        if not a:
            return
        await self.message.edit(
            embed=Embed(
                color=0xFFFFFF,
                description="You picked Charmander\nUse `.dex charmander` to get more info about it!",
            ),
            view=None,
            files=[],
        )

    @button(emoji="<:squirtle:937042783804473384>", style=ButtonStyle.blurple)
    async def squirtle(self, button: Button, interaction: MessageInteraction):
        await interaction.response.defer()
        a = await self.insert_into_database(interaction.author.id, "squirtle")
        if not a:
            return
        await self.message.edit(
            embed=Embed(
                color=0xFFFFFF,
                description="You picked Squirtle\nUse `.dex squirtle` to get more info about it!",
            ),
            view=None,
            files=[],
        )
