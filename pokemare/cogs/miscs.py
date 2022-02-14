import aiohttp
import asyncio
import random

from PokeMare.pokemare.songs import SongList
from PokeMare.pokemare.trivia import TriviaList
from PokeMare.pokemare.trivia import TriviaButtons

from disnake.file import File
from disnake.colour import Color
from disnake.embeds import Embed
from disnake.ext.commands.bot import Bot
from disnake.ext.commands.cog import Cog
from disnake.ext.commands.core import command
from disnake.ext.commands.core import cooldown
from disnake.ext.commands.core import BucketType
from disnake.ext.commands.core import CommandOnCooldown
from disnake.ext.commands.context import Context
from disnake.ui import Button, View


class Miscs(Cog, name="Misc Commands"):
    """Other in-game fun commands :3"""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.hidden = False
        self.emoji = ""
        self.session = aiohttp.ClientSession()
        self.song_list = SongList()
        self.song_list.load_from_json()
        self.trivia_list = TriviaList()
        self.trivia_list.load_from_json()

    @command(name="trivia", description='Receive a random trivia question!')
    @cooldown(1, 30, BucketType.user)
    async def trivia_command(self, ctx: Context):
        trivia = self.trivia_list.get_random_trivia()
        random.shuffle(trivia.options)
        if trivia:
            options_string = "**A.}** " + trivia.options[0] + "\n**B.}** " + \
                             trivia.options[1] + "\n**C.}** " + trivia.options[2] + "\n**D.}** " + trivia.options[3]
            embed = Embed(
                title=trivia.question,
                description=options_string,
                color=ctx.bot.color,
            )
            embed.set_footer(
                text=f"Trivia for {ctx.author}",
                icon_url=ctx.author.display_avatar,
            )
            embed.set_thumbnail(url="https://www.fortbend.lib.tx.us/sites/default/files/2021-05/pokemon.png")
            if trivia.question_type == "multiple choice":
                answer_index = trivia.options.index(trivia.answer)
                view = TriviaButtons(answer_index, ctx.author)
                message = await ctx.reply(embed=embed, view=view)
                await view.wait()
                if view.correct:
                    embed = Embed(
                        title="You got it correct!",
                        description=trivia.response + "\n\nReceived <:pokedollar:941929762912342027>?? PokéDollars",
                        color=Color.green(),
                    )
                    embed.set_footer(
                        text=f"Trivia for {ctx.author}",
                        icon_url=ctx.author.display_avatar,
                    )
                    embed.set_thumbnail(url="https://www.fortbend.lib.tx.us/sites/default/files/2021-05/pokemon.png")
                    await message.edit(embed=embed, view=View())
                else:
                    embed = Embed(
                        title="Sorry, you got it wrong!",
                        description="Correct Answer:\n\n" + trivia.response + "\n\nPlease try again later!",
                        color=Color.red(),
                    )
                    embed.set_footer(
                        text=f"Trivia for {ctx.author}",
                        icon_url=ctx.author.display_avatar,
                    )
                    embed.set_thumbnail(url="https://www.fortbend.lib.tx.us/sites/default/files/2021-05/pokemon.png")
                    await message.edit(embed=embed, view=View())

    @trivia_command.error
    async def trivia_command_error(self, ctx: Context, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.reply("Trivia not available. " + str(error) + ".")

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