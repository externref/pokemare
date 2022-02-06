from disnake.embeds import Embed
from disnake.ext.commands.bot import Bot
from disnake.ext.commands.cog import Cog
from disnake.ext.commands.core import command 
from disnake.ext.commands.context import Context


class General(Cog, name='General Commands'):
    """Some usual bot commands"""

    def __init__(self , bot:Bot):
        self.hidden =False
        self.emoji = '😁'
        self.bot = bot
    
    @command(name='info',aliases=['menu'])
    async def _menu(self , ctx : Context):
        prefix = await self.bot.get_prefix(ctx.message)
        desc=f"""
Hey! {ctx.author} My prefix is: {prefix[2]} | {prefix[2]}help

**Ping** : `{round(ctx.bot.latency*1000 , 2)}ms`
**Uptime** :
**Trainers** : {len(ctx.bot.users)}
Join this Official Server [Here]({ctx.bot.support_server_invite_url})!

**About PokéMare** :

PokéMares a fan made discord Pokémon bot made by `Realer#0511`, & `Sarthak\_#0460` the bot is made purely for enjoyment! But if you ever decide to donate, to help out with the bots costly funds please do so []!

Pokémon Copyright ©️ 1995 - 2021 Nintendo/Creatures Inc./GAME FREAK Inc.
Pokémon And All Respective Names are Trademarks of Nintendo 1996 - 2022
Pokémare is not affiliated with Nintendo, Creatures Inc. and GAME FREAK Inc.
""" 
        embed = Embed(
            description=desc,
            color=ctx.bot.color
        ).set_author(name='PokéMare')#.set_image(url='https://media.discordapp.net/attachments/936820715938795561/937542712473812992/image0.gif')
        await ctx.reply(embed=embed)

    @command(name='ping',description='Latency of the Bot')
    async def _ping(self , ctx : Context):
        """Pong"""
        await ctx.send(f"🏓 `{round(ctx.bot.latency*1000 , 2)}ms` Pong ! ")

    @command(name='invite',description='Invite the bot to your servers!')
    async def _invite(self , ctx : Context):
        """Bot invite"""
        await ctx.send(f"> The bot is still in a development stage! You would like to test it out so we have made the invite link available",
        embed = Embed(color=ctx.bot.color,description=f'> {ctx.bot.get_emoji(866957054278631444)} Invite Bot by [`clicking here`]({ctx.bot.invite_url})\n> ♥️ We have a [`support server`]({ctx.bot.support_server_invite_url}) too'))


def setup(bot : Bot):
    bot.add_cog(General(bot))