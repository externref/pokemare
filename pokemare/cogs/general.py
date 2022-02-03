from disnake.embeds import Embed
from disnake.ext.commands.bot import Bot
from disnake.ext.commands.cog import Cog
from disnake.ext.commands.core import command 
from disnake.ext.commands.context import Context


class General(Cog, name='General Commands'):
    """Some usual bot commands"""

    def __init__(self , bot):
        self.hidden =False
        self.emoji = '😁'
        self.bot = bot
    
    @command(name='ping',description='Latency of the Bot')
    async def _ping(self , ctx : Context):
        """Pong"""
        await ctx.send(f"🏓 {round(ctx.bot.latency , 2)} Pong ! ")

    @command(name='invite',description='Invite the bot to your servers!')
    async def _invite(self , ctx : Context):
        """Bot invite"""
        await ctx.send(f"> The bot is still in a development stage! You would like to test it out so we have made the invite link available",
        embed = Embed(color=ctx.bot.color,description=f'> {ctx.bot.get_emoji(866957054278631444)} Invite Bot by [`clicking here`]({ctx.bot.invite_url})\n> ♥️ We have a [`support server`]({ctx.bot.support_server_invite_url}) too'))


def setup(bot : Bot):
    bot.add_cog(General(bot))