from __future__ import annotations

from discord.message import Message
from discord.ext.commands.context import Context
from discord.ext.commands.bot import Bot, when_mentioned_or


from aiosqlite import Connection, connect


class PrefixHandler:
    async def connect(self) -> Connection:
        self.database = await connect("prefixes.db")
        async with self.database.cursor() as cursor:
            await cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS prefixes
                ( guild_id TEXT, prefix TEXT )
                """
            )
            await self.database.commit()
        return self.database

    async def get_prefix(self, bot: Bot, message: Message | Context) -> list[str]:
        if isinstance(message, Context):
            message = message.message

        prefix = "."
        async with self.database.cursor() as cursor:
            await cursor.execute(
                """
                SELECT * FROM prefixes
                WHERE guild_id = ?
                """,
                (str(message.guild.id),),
            )
            row = await cursor.fetchone()
            if row:
                prefix = row[1]
        return when_mentioned_or(prefix)(bot, message)

    async def set_prefix(self, message: Message | Context, prefix: str) -> None:
        async with self.database.cursor() as cursor:
            exists: bool = await self.get_prefix(None, message)
            if exists:
                await cursor.execute(
                    """
                    UPDATE prefixes
                    SET prefix = ?
                    WHERE guild_id = ?
                    """,
                    (prefix, str(message.guild.id)),
                )
            else:
                await cursor.execute(
                    """
                    INSERT INTO prefixes
                    guild_id , prefix
                    VALUES (?, ?)
                    """,
                    (str(message.guild.id, prefix)),
                )
        await self.database.commit()
