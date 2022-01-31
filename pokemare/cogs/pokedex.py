from typing import Union
from disnake.ext.commands.bot import Bot
from disnake.ext.commands.cog import Cog
from disnake.ext.commands.core import command
from disnake.ext.commands.context import Context

class Pokedex(Cog , name='Pokedex'):
    def __init__(self , bot : Bot):
        self.bot = bot
        
    @command(name='pokedex',description='Lookup for a pokemon in the pokedex',aliases=['dex'])
    async def pokedex(self , ctx : Context , pokemon : Union[int, str]):
        ...