from __future__ import annotations

import datetime
import json
import os

import disnake
import dotenv
from disnake.ext import commands

from database import GuessThePokemonDatabase


class PokeMare(commands.Bot):
    boot_time: datetime.datetime

    def __init__(self) -> None:
        intents = disnake.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(
            command_prefix="p!",
            #test_guilds=[],
            intents=intents,
            strip_after_prefix=True,
            case_insensitive=True,
            help_command=None
        )
        self.gtp_db = GuessThePokemonDatabase()
        self.load_extension("jishaku")
        self.get_cog("Jishaku").ignored = True
        self.load_extensions("pokemare/cogs")
        with open("data/pokemons.json", "r") as file:
            self.pokemon_dict: dict = json.load(file)

    async def on_ready(self) -> None:
        print("Bot is online!")
        await self.setup()

    async def setup(self) -> None:
        self.boot_time = datetime.datetime.now()
        await self.gtp_db.setup(self)
        await self.wait_until_ready()
        await self.change_presence(
            activity=disnake.Activity(
                type=disnake.ActivityType.listening, name="/help"
            ),
            status=disnake.Status.idle,
        )

    async def get_prefix(self, message: disnake.Message) -> list[str]:
        return commands.when_mentioned_or("p!")(self, message)

    def run(self) -> None:
        dotenv.load_dotenv()
        super().run(os.getenv("TOKEN"))

    @property
    def uptime(self) -> datetime:
        return datetime.datetime.now() - self.boot_time

    @property
    def invite_url(self) -> str:
        return f"https://discord.com/api/oauth2/authorize?client_id={self.user.id}&permissions=378025593921&scope=bot%20applications.commands"
