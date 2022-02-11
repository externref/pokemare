import aiohttp
import asyncio
import random

from PokeMare.pokemare.songs import SongList

from disnake.file import File
from disnake.colour import Color
from disnake.embeds import Embed
from disnake.ext.commands.bot import Bot
from disnake.ext.commands.cog import Cog
from disnake.ext.commands.core import command
from disnake.ext.commands.context import Context


class Miscs(Cog, name="Misc Commands"):
    """Other in-game fun commands :3"""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.hidden = False
        self.emoji = ""
        self.session = aiohttp.ClientSession()
        self.song_list = SongList()
        self.song_list.load_from_json("songs.json")

    @command(name="lyrics", description='Recite the lyrics to our Pokemon anthem!')
    async def lyrics_command(self, ctx: Context, *, song_name: str = "Gotta Catch 'Em All"):
        song = self.song_list.get_song_by_name(song_name)
        if song:
            embed = Embed(
                title=song.title,
                description="**Artist**: " + song.artist +
                            "\n**Album**: " + song.album +
                            "\n**Released**: " + song.release_year +
                            "\n**[Youtube Link](" + song.link + ")**"
                            "\n\n" + song.lyrics + "\n\n",
                color=ctx.bot.color,
            )
            embed.set_image(url=song.image)
            await ctx.reply(embed=embed)
        else:
            await ctx.reply("No song found with title '" + song_name + "'.")

    @command(name="guessthepokemon", aliases=["gtp"], description='Guess the pokemon from the shadow in the image for rewards!')
    async def guess_the_pokemon(self, ctx: Context):
        """Guess for reward"""
        pokemon_id = random.randint(1, 152)
        pokemon_name = (
            await (
                await self.session.get(
                    f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
                )
            ).json()
        )["name"]
        file = File(
            f"images/hidden_pokemons/{pokemon_id}.png", filename="pokemon_guess.png"
        )
        embed = Embed(
            title="Guess The Pokemon",
            description="Send the name of the pokemon in this channel ( within 60 seconds )",
            color=ctx.bot.color,
        )
        embed.set_image(url="attachment://pokemon_guess.png")
        await ctx.reply(embed=embed, file=file)

        try:
            await self.bot.wait_for(
                "message",
                check=lambda m: m.author == ctx.author
                and m.content.lower() == pokemon_name,
                timeout = 60
            )
            embed = Embed(
                color=Color.green(),
                description=f"GG, you guessed the right pokemon {pokemon_name.upper()}",
            )
            embed.set_image(url="attachment://pokemon_guess.png")
            file = File(
                f"images/revealed_pokemons/{pokemon_id}.png",
                filename="pokemon_guess.png",
            )
            await ctx.send(embed=embed, file=file)
        except asyncio.TimeoutError:
            embed = Embed(
                color=Color.red(),
                description=f"{ctx.author.name}, you didnt answer on time or your answer were wrong!\nThe pokemon is ||{pokemon_name.upper()}||",
            )
            embed.set_image(url="attachment://pokemon_guess.png")
            file = File(
                f"images/revealed_pokemons/{pokemon_id}.png",
                filename="pokemon_guess.png",
            )
            await ctx.send(embed=embed, file=file)


def setup(bot: Bot):
    bot.add_cog(Miscs(bot))