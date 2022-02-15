import asyncio
from typing import Optional


from disnake.colour import Color
from disnake.embeds import Embed
from disnake.message import Message
from disnake.enums import ButtonStyle
from disnake.ext.commands.cog import Cog
from disnake.ui import View, Button, button

# from disnake.ext.commands.core import command
from disnake.interactions import MessageInteraction
from disnake.ext.commands.slash_core import slash_command
from disnake.interactions import ApplicationCommandInteraction, MessageInteraction


from .. import PokeMare

DESC = """
<:moonball:918870698997452831> Welcome to the world of **PokéMare**, and the start of your Pokémon Journey!
Register your trainer account, by picking one of these three starter Pokémon!

<:Bulbasaur:936975459688779776> : **Bulbasaur** | <:Charmander:936975190468997120> : **Charmander** | <:squirtle:937042783804473384> : **Squirtle**
"""

CLAIMED = """
Congratulations on the start of your PokéMare Journey! You and your **$pokemon** will be the best of buddy’s, I just know it!

Here’s a gift to start off your adventure: 
 x10  x3  <:potion:941956192010371073> x1
"""


class Start(Cog, name="Startup Command"):
    """Start with your PokéMare journey !"""

    def __init__(self, bot: PokeMare) -> None:
        self.hidden = False
        self.emoji = "<:trainer:937618424169914398>"
        self.bot = bot

    @slash_command(
        name="start",
        description="Begin your pokemon journey!"
    )
    async def start_slash_command(
        self, interaction: ApplicationCommandInteraction
    ) -> Optional[Message]:
        data = await self.bot.user_database.get_user_information(
            str(interaction.author.id)
        )
        if data:
            return await interaction.response.send_message(
                embed=Embed(
                    title="Professor Oak....",
                    description=f"You have already chose your starter pokemon with ID `{data[2]}`!",
                    color=self.bot.color,
                ).set_thumbnail(
                    url="https://media.discordapp.net/attachments/872567465157201961/872575401891889172/start.png"
                )
            )
        embed = Embed(color=0xFFFFFF, description=DESC, title="Professor Oak")
        embed.set_image(
            "https://media.discordapp.net/attachments/937603105443442769/937603206534549514/choose_pokemon.png"
        )
        embed.set_footer(text="You have 30 seconds to respond")
        my_view = SelectPokemon(self.bot, interaction)
        await interaction.send(embed=embed, view=my_view)


def setup(bot: PokeMare):
    bot.add_cog(Start(bot))


class SelectPokemon(View):
    def __init__(self, bot, inter):
        self.bot: PokeMare = bot
        self.inter: ApplicationCommandInteraction = inter
        super().__init__(timeout=30)

    async def insert_into_database(self, user_id: int, pokemon: str):
        view = View()
        view.add_item(Button(style=ButtonStyle.green, label="Confirm"))
        embed = Embed(
            color=0xFFFFFF,
            description=f"Oh? **{pokemon.title()}**, a fine choice! Confirm your pick by clicking on `Confirm` ",
        ).set_thumbnail(
            url=self.bot.pokemon_dict[pokemon.lower()]["sprites"]["animated"]
        )
        message = await self.inter.channel.send(view=view, embed=embed)
        try:
            res: MessageInteraction = await self.bot.wait_for(
                "button_click",
                check=lambda m: m.author.id == user_id and m.message == message,
                timeout=30,
            )
            await res.response.defer()
        except asyncio.TimeoutError:
            return await self.inter.channel.send(
                f"<@!{user_id}> you didn't respond on time !"
            )
        await self.bot.user_database.insert_user_into_database(
            user_id, "m", self.bot.pokemon_dict[pokemon.lower()]["id"]
        )
        await message.channel.send(
            embed=Embed(
                description=CLAIMED.replace("$pokemon", pokemon.title()),
                color=Color.green(),
            ).set_thumbnail(
                url=self.bot.pokemon_dict[pokemon.lower()]["sprites"]["animated"]
            )
        )

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
        await self.inter.channel.send(
            embed=Embed(
                color=0xFFFFFF,
                description="You picked Bulbasaur\nUse `.dex bulbasaur` to get more info about it!",
            ),
            view=None,
        )

    @button(emoji="<:Charmander:936975190468997120>", style=ButtonStyle.red)
    async def charmander(self, button: Button, interaction: MessageInteraction):
        await interaction.response.defer()
        a = await self.insert_into_database(interaction.author.id, "charmander")
        if not a:
            return
        await self.inter.channel.send(
            embed=Embed(
                color=0xFFFFFF,
                description="You picked Charmander\nUse `.dex charmander` to get more info about it!",
            ),
            view=None,
        )

    @button(emoji="<:squirtle:937042783804473384>", style=ButtonStyle.blurple)
    async def squirtle(self, button: Button, interaction: MessageInteraction):
        await interaction.response.defer()
        a = await self.insert_into_database(interaction.author.id, "squirtle")
        if not a:
            return
        await self.inter.channel.send(
            embed=Embed(
                color=0xFFFFFF,
                description="You picked Squirtle\nUse `.dex squirtle` to get more info about it!",
            ),
            view=None,
        )
