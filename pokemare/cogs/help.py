import disnake
from disnake.ext import commands

from ..bot import PokeMare


class ObjNotFound(Exception):
    ...


class HelpCommand(commands.Cog):
    def __init__(self, bot: PokeMare) -> None:
        self.bot = bot
        self.ignored = True
        super().__init__()

    @property
    def desc(self) -> str:
        return (
            f"🌙 What's Pokemare ?\nUse : `/menu` to get a brief info\n\n"
            + f" [`Invite Bot`]({self.bot.invite_url}) | [`Support Server`](https://discord.gg/Km8WwHBSrg)"
        )

    async def send_bot_help(self, interaction: disnake.AppCommandInter) -> None:
        embed = (
            disnake.Embed(
                color=disnake.Color.blurple(),
                description=self.desc,
            )
            .set_author(name=self.bot.user, icon_url=self.bot.user.display_avatar)
            .set_thumbnail(url=self.bot.user.display_avatar)
        )
        for cog in self.bot.cogs.values():
            if getattr(cog, "ignored", None):
                continue
            embed.add_field(
                name=f"{cog.qualified_name.upper()} COMMANDS",
                value=f"{cog.description}\n`/{'` , `/'.join(c.name for c in cog.get_slash_commands())}`",
                inline=False,
            )

        view = disnake.ui.View()
        view.add_item(
            disnake.ui.Button(
                style=disnake.ButtonStyle.link,
                label="Invite",
                emoji="🤍",
                url=self.bot.invite_url,
            )
        )
        view.add_item(
            disnake.ui.Button(
                style=disnake.ButtonStyle.link,
                label="Invite",
                emoji=self.bot.get_emoji(866894907741831218),
                url="https://discord.gg/Km8WwHBSrg",
            ),
        )
        await interaction.edit_original_message(embed=embed, view=view)

    async def send_command_help(
        self,
        interaction: disnake.AppCommandInter,
        command: commands.InvokableSlashCommand,
    ) -> None:
        embed = disnake.Embed(
            description=command.description, color=disnake.Color.yellow()
        )
        embed.set_author(
            name=f"/{command.name.upper()} COMMAND",
            icon_url=self.bot.user.display_avatar,
        )
        await interaction.edit_original_message(embed=embed)

    @commands.slash_command(name="help", description=f"Help for commands")
    async def _help(self, interaction: disnake.AppCommandInter, command: str = None):
        if command and self.bot.get_slash_command(command) is None:
            return await interaction.send(
                embed=disnake.Embed(
                    color=disnake.Color.red(),
                    description=f"This command does not exist.",
                )
            )

        await interaction.response.defer()
        try:
            if not command:
                return await self.send_bot_help(interaction)

            slash_cmd = self.bot.get_slash_command(command)
            if slash_cmd and isinstance(slash_cmd, commands.InvokableSlashCommand):
                return await self.send_command_help(interaction, slash_cmd)

            raise ObjNotFound

        except ObjNotFound:
            await interaction.send(
                embed=disnake.Embed(
                    color=disnake.Color.red(), description=f"Unable to send help."
                )
            )

    @_help.autocomplete("command")
    async def command_autocompletes(
        self, interaction: disnake.AppCommandInter, string: str
    ) -> list[str]:
        return [
            c.name
            for c in self.bot.slash_commands
            if c.name.startswith(string.lower()) and c != "help"
        ]


def setup(bot: PokeMare) -> None:
    bot.add_cog(HelpCommand(bot))
