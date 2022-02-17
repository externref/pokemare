import aiohttp
import asyncio
import random

from disnake.file import File
from disnake.colour import Color
from disnake.embeds import Embed
from disnake.ext.commands.cog import Cog
from disnake.ext.commands.core import command
from disnake.ext.commands import slash_command
from disnake.ext.commands.core import cooldown
from disnake.ext.commands.context import Context
from disnake.ext.commands.core import BucketType
from disnake.ext.commands.slash_core import Option
from disnake.ext.commands.core import CommandOnCooldown
from disnake.interactions import ApplicationCommandInteraction

from .. import PokeMare
from ..songs import SongList
from ..trivia import TriviaList, TriviaButtons
from ..mail import MailBoxUIManager


class Miscs(Cog, name="Misc Commands"):
    """Other in-game fun commands :3"""

    def __init__(self, bot: PokeMare):
        self.bot = bot
        self.hidden = False
        self.emoji = ""
        self.session = aiohttp.ClientSession()
        self.song_list = SongList()
        self.song_list.load_from_json()
        self.trivia_list = TriviaList()
        self.trivia_list.load_from_json()

        # TODO: Remove temporary mail testing stuff once we have proper user classes and database and shit
        #self.temporary_user_dict_for_mail = mailbox_dict

    @slash_command(
        name="mail", description="Send and receive mail in your personal mailbox.", guild_ids=[303282588901179394]
    )
    async def mail_command(self, inter: ApplicationCommandInteraction):
        user = await self.bot.user_database.get_user(inter.author.id)
        if user:
            mailbox = user.mailbox
            mailbox.update_fields()
            mailbox_manager = MailBoxUIManager(self.bot, user, mailbox)
            await mailbox_manager.start(inter)
        else:
            await inter.send("You have not started the bot yet! Please do `/start`!")

    @slash_command(
        name="trivia", description="Take the trivia quiz and earn Pokedollars!"
    )
    @cooldown(1, 30, BucketType.user)
    async def trivia_command(self, inter: ApplicationCommandInteraction):
        trivia = self.trivia_list.get_random_trivia()
        random.shuffle(trivia.options)
        if trivia:
            options_string = (
                "**A.}** "
                + trivia.options[0]
                + "\n**B.}** "
                + trivia.options[1]
                + "\n**C.}** "
                + trivia.options[2]
                + "\n**D.}** "
                + trivia.options[3]
            )
            embed = Embed(
                title=trivia.question,
                description=options_string,
                color=inter.bot.color,
            )
            embed.set_footer(
                text=f"Trivia for {inter.author}",
                icon_url=inter.author.display_avatar,
            )
            embed.set_thumbnail(
                url="https://www.fortbend.lib.tx.us/sites/default/files/2021-05/pokemon.png"
            )
            if trivia.question_type == "multiple choice":
                answer_index = trivia.options.index(trivia.answer)
                view = TriviaButtons(answer_index, inter.author)
                await inter.response.send_message(embed=embed, view=view)
                await view.wait()
                if view.correct:
                    embed = Embed(
                        title="You got it correct!",
                        description=trivia.response
                        + "\n\nReceived <:pokedollar:941929762912342027>?? PokéDollars",
                        color=Color.green(),
                    )
                    embed.set_footer(
                        text=f"Trivia for {inter.author}",
                        icon_url=inter.author.display_avatar,
                    )
                    embed.set_thumbnail(
                        url="https://www.fortbend.lib.tx.us/sites/default/files/2021-05/pokemon.png"
                    )
                    await inter.edit_original_message(embed=embed, view=None)
                else:
                    embed = Embed(
                        title="Sorry, you got it wrong!",
                        description="Correct Answer:\n\n"
                        + trivia.response
                        + "\n\nPlease try again later!",
                        color=Color.red(),
                    )
                    embed.set_footer(
                        text=f"Trivia for {inter.author}",
                        icon_url=inter.author.display_avatar,
                    )
                    embed.set_thumbnail(
                        url="https://www.fortbend.lib.tx.us/sites/default/files/2021-05/pokemon.png"
                    )
                    await inter.edit_original_message(embed=embed, view=None)

    @trivia_command.error
    async def trivia_command_error(self, inter: ApplicationCommandInteraction, error):
        if isinstance(error, CommandOnCooldown):
            await inter.send("Trivia not available. " + str(error) + ".")

    @slash_command(
        name="lyrics",
        description="Get lyrics to your favorite Pokemon themes!",
        options=[Option("song_name", description="Name of the song")],
    )
    async def lyrics_command(
        self,
        inter: ApplicationCommandInteraction,
        song_name: str = "Gotta Catch 'Em All",
    ):
        song = self.song_list.get_song_by_name(song_name)
        if song:
            embed = Embed(
                title=song.title,
                description="**Artist**: "
                + song.artist
                + "\n**Album**: "
                + song.album
                + "\n**Released**: "
                + song.release_year
                + "\n**[Youtube Link]("
                + song.link
                + ")**"
                "\n\n" + song.lyrics + "\n\n",
                color=inter.bot.color,
            )
            embed.set_image(url=song.image)
            await inter.send(embed=embed)
        else:
            await inter.send("No song found with title '" + song_name.title() + "'.")

    @command(
        name="guessthepokemon",
        aliases=["gtp"],
        description="Guess the pokemon from the shadow in the image for rewards!",
    )
    @cooldown(1, 30, BucketType.user)
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
            title="Who's that Pokemon?!",
            description="Send the name of the pokemon in this channel\n(within 60 seconds)",
            color=ctx.bot.color,
        )
        embed.set_image(url="attachment://pokemon_guess.png")
        await ctx.reply(embed=embed, file=file)

        try:
            await self.bot.wait_for(
                "message",
                check=lambda m: m.author == ctx.author
                and m.content.lower() == pokemon_name,
                timeout=60,
            )
            embed = Embed(
                color=Color.green(),
                description=f"Congratulations, you guessed the correct Pokemon: {pokemon_name.upper()}!",
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
                description=f"{ctx.author.name}, you didn't answer on time or your answer was wrong!\nThe correct Pokemon was ||{pokemon_name.upper()}!||",
            )
            embed.set_image(url="attachment://pokemon_guess.png")
            file = File(
                f"images/revealed_pokemons/{pokemon_id}.png",
                filename="pokemon_guess.png",
            )
            await ctx.send(embed=embed, file=file)

    @guess_the_pokemon.error
    async def guess_the_pokemon_error(self, ctx: Context, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.reply("'Guess the Pokemon' not available. " + str(error) + ".")


def setup(bot: PokeMare):
    bot.add_cog(Miscs(bot))
