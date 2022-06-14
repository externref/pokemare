from __future__ import annotations

import aiomysql
import disnake
from disnake.ext import commands


class GuessThePokemonDatabase:
    bot: commands.Bot
    database_pool: aiomysql.Pool

    async def exec_write_operation(self, sql: str, values: tuple = None) -> None:

        async with self.database_pool.acquire() as conn:
            conn: aiomysql.Connection
            async with conn.cursor() as cursor:
                cursor: aiomysql.Cursor
                await cursor.execute(sql, values)
            await conn.commit()

    async def exec_fetchall(self, sql: str, values: tuple = None) -> list[tuple]:
        async with self.database_pool.acquire() as conn:
            conn: aiomysql.Connection
            async with conn.cursor() as cursor:
                cursor: aiomysql.Cursor
                await cursor.execute(sql, values)
                return await cursor.fetchall()

    async def exec_fetchone(self, sql: str, values: tuple = None) -> tuple:
        async with self.database_pool.acquire() as conn:
            conn: aiomysql.Connection
            async with conn.cursor() as cursor:
                cursor: aiomysql.Cursor
                await cursor.execute(sql, values)
                return await cursor.fetchone()

    async def setup(self, bot: commands.Bot) -> None:

        self.database_pool = bot.database_pool
        self.bot = bot

        await self.exec_write_operation(
            """
            CREATE TABLE IF NOT EXISTS guesses
            ( user_id BIGINT, guild_id BIGINT, guesses INT ) ;
            """
        )

    async def local_leaderboard(self, guild: disnake.Guild) -> list[tuple]:
        cursor = await self.connection.cursor()
        await cursor.execute(
            """
            SELECT user_id, guesses FROM guesses
            ORDER BY guesses DESC
            WHERE guild_id = %s
            """,
            (guild.id,),
        )
        raw = await cursor.fetchall()
        users = [
            (self.bot.get_user(id_), guesses)
            for id_, guesses in raw
            if self.bot.get_user(id_)
        ]
        return users

    async def global_leaderboard(self) -> list[tuple]:
        raw = await self.exec_fetchall(
            """
            SELECT user_id, SUM(guesses) FROM guesses
            GROUP BY user_id
            ORDER BY SUM(guesses) DESC
            """
        )
        # list(raw).sort(key= lambda t: t[1])
        users = [
            (self.bot.get_user(data[0]), data[1])
            for data in raw
            if self.bot.get_user(data[0] or await self.bot.fetch_user(data[0]))
        ]
        return users

    async def get_data_for_member(self, member: disnake.Member):
        data = await self.exec_fetchall(
            """
            SELECT * FROM guesses
            WHERE user_id = %s AND guild_id = %s
            """,
            (member.id, member.guild.id),
        )
        return data

    async def get_guesses_for_user(self, user: disnake.User):
        data = await self.exec_fetchone(
            "SELECT SUM(guesses) FROM guesses WHERE user_id = %s", (user.id,)
        )
        return data[0] if data else 0

    async def add_guess(self, member: disnake.Member):
        values = (
            member.id,
            member.guild.id,
        )
        if await self.get_data_for_member(member):
            await self.exec_write_operation(
                """
                UPDATE guesses
                SET guesses = guesses + 1
                WHERE user_id = %s AND guild_id = %s
                """,
                values,
            )
        else:
            await self.exec_write_operation(
                """
                INSERT INTO guesses
                VALUES ( %s, %s, 1 )
                """,
                values,
            )
