from __future__ import annotations

import os
import json
from datetime import datetime

from discord.flags import Intents
from discord.message import Message
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context

from .handlers import PrefixHandler


class PokeMare(Bot):
    def __init__(self) -> None:
        self.prefix_database = PrefixHandler()
        self.boot_time = datetime.now()
        self.color = 0x04356D
        self.support_server_invite_url = os.getenv("SUPPORT_SERVER")
        intents = Intents.all()
        super().__init__(
            command_prefix=self.prefix_database.get_prefix,
            intents=intents,
            case_insensitive=True,
        )
        self.load_extension("jishaku")
        self.load_extensions_from("pokemare.plugins")
        with open("data/pokemons.json", "r") as file:
            self.pokemon_dict = json.load(file)

    def load_extensions_from(self, path: str) -> None:
        for file in os.listdir(path):
            if not file.startswith("_") and file.endswith(".py"):
                self.load_extension(path + file[:-3])

    async def on_ready(self) -> None:
        self.prefix_database.connect()

    async def getch_user(self, id: int) -> None:
        return self.get_user(id) or await self.fetch_user(id)

    async def set_prefix_for(self, message: Message | Context, prefix: str) -> None:
        await self.prefix_database.set_prefix(message, prefix)
