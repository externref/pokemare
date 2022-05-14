from __future__ import annotations

import aiosqlite
import disnake
from disnake.ext import commands


class GuessThePokemonDatabase:
    bot: commands.Bot
    connection: aiosqlite.Connection

    async def setup(self, bot: commands.Bot) -> None:
        connection = await aiosqlite.connect("gtpdatabase.db")
        await connection.execute(
            """
            CREATE TABLE IF NOT EXISTS guesses
            ( user_id BIGINT, guild_id BIGINT, guesses INT ) ;
            """
        )
        await connection.commit()
        self.bot = bot
        self.connection = connection

    async def local_leaderboard(self, guild: disnake.Guild) -> list[tuple]:
        cursor = await self.connection.cursor()
        await cursor.execute(
            """
            SELECT user_id, guesses FROM guesses
            ORDER BY guesses DESC
            WHERE guild_id = ?
            """,
            (guild.id,),
        )
        raw = await cursor.fetchall()
        users = [
            (self.bot.get_user(id), guesses)
            for id, guesses in raw
            if self.bot.get_user(id)
        ]
        return users

    async def global_leaderboard(self) -> list[tuple]:
        cursor = await self.connection.cursor()
        await cursor.execute(
            """
            SELECT user_id, guesses FROM guesses
            ORDER BY guesses DESC
            """
        )
        raw = await cursor.fetchall()
        users = [
            (self.bot.get_user(data[0]), data[1])
            for data in raw
            if self.bot.get_user(data[0])
        ]
        return users

    async def get_data_for_member(self, member: disnake.Member):
        cursor = await self.connection.cursor()
        await cursor.execute(
            """
            SELECT * FROM guesses
            WHERE user_id = ? AND guild_id = ?
            """,
            (member.id, member.guild.id),
        )
        return await cursor.fetchall()

    async def add_guess(self, member: disnake.Member):
        cursor = await self.connection.cursor()
        values = (
            member.id,
            member.guild.id,
        )
        if await self.get_data_for_member(member):
            await cursor.execute(
                """
                UPDATE guesses
                SET guesses = guesses + 1
                WHERE user_id = ? AND guild_id = ?
                """,
                values,
            )
        else:
            await cursor.execute(
                """
                INSERT INTO guesses
                VALUES ( ?, ?, 1 )
                """,
                values,
            )

        await self.connection.commit()
