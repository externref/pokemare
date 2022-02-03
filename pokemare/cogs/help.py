from disnake.ext.commands.bot import Bot   
from disnake.ext.commands.cog import Cog 
from disnake.ext.commands.context import Context
from disnake.ext.commands.core import command , Command
from disnake.ext.commands.help import HelpCommand
from disnake.embeds import Embed
from disnake.ui import Button, View
from disnake.enums import ButtonStyle

class HelpMaker(Cog):
    def __init__(self , bot:Bot ):
        self.hidden = True
        self.bot = bot
        bot.help_command = MyCustomHelp()

    @command(name='h')
    async def _short_help(self , ctx : Context , * , obj = None):
        if obj:
            await ctx.send_help(obj)
        else : 
            await ctx.send_help()

def setup(bot:Bot):
    bot.add_cog(HelpMaker(bot))



class MyCustomHelp(HelpCommand):

    async def command_signature(self,command):
        command_signature = ""
        for arg in command.signature.split("] ["):
            if "=" in arg:
                parsed_arg = "{" + arg.split("=")[0].strip("[]<>]") + "}"
            else:
                parsed_arg = "[" + arg.strip("[]<>") + "]"
                if parsed_arg == "[]":
                    parsed_arg = ""
            command_signature += parsed_arg + " "

        return command_signature

    async def send_bot_help(self, mapping):
        _bot : Bot = self.context.bot
        embed = Embed(
            description=f"**🌙 What's Pokemare ?**\nUse : `{(await _bot.get_prefix(self.context.message))[2]}menu` to get a brief info",
            color = 0x04356d
        )
        embed.set_author(name=_bot.user.name.upper()+' HELP')
        embed.set_footer(text=f'Requested by {self.context.author}',icon_url=self.context.author.display_avatar)
        embed.set_thumbnail(url=_bot.user.display_avatar)
        for cog in _bot.cogs:
            cog : Cog = _bot.get_cog(cog)
            if cog.hidden: continue
            embed.add_field(name=f'{cog.emoji} {cog.qualified_name}', value=f"{cog.__doc__}\n`{'` , `'.join(command.name for command in cog.get_commands())}`",inline=False)
        view = View()
        view.add_item(Button(label='Invite',emoji=_bot.get_emoji(866894907741831218),url=_bot.invite_url,style=ButtonStyle.url))
        view.add_item(Button(label='Support',emoji='♥️',url=_bot.support_server_invite_url,style=ButtonStyle.url))
        await self.context.reply(embed=embed,view=view)

    async def send_command_help(self, command: Command):
        print('tiggered')
        help_dict = {
            "Name": command.name,
            "Aliases": " , ".join(command.aliases) or "No aliases",
            "Description": command.description.replace("        ", ""),
            "Usage": "```ini\n"
            + (await self.context.bot.get_prefix(self.context.message))[2]
            + command.name
            + " "
            + await self.command_signature(command)
            + "```",
        }
        desc = "\n".join("**" + key + " :** " + help_dict[key] for key in help_dict)
        embed = Embed(
            description=desc, color=0x04356d
        )
        embed.set_author(
            name=f"{command.name.upper()} COMMAND",
            icon_url=self.context.bot.user.display_avatar,
        )
        embed.set_footer(
            text=f"Requested by {self.context.author}",
            icon_url=self.context.author.display_avatar,
        )
        await self.context.reply(embed=embed)

    async def send_cog_help(self, cog):
        return await super().send_cog_help(cog)
    
