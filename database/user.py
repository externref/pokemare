from __future__ import annotations

import aiomysql
import disnake
from disnake.ext import commands


class Currency:
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
            CREATE TABLE IF NOT EXISTS currency
            ( user_id BIGINT, coins INT )
            """
        )

    async def get_coins_for(self, user_id: int) -> int:
        data = await self.exec_fetchone(
            """
            SELECT * FROM currency 
            WHERE user_id = %s
            """,
            (user_id,),
        )
        return data[1] if data else 0

    async def add_coins_to(self, user_id: int, coins: int) -> None:
        if not await self.get_coins_for(user_id):
            await self.exec_write_operation(
                """
                INSERT INTO currency 
                VALUES ( %s, %s )
                """,
                (user_id, coins),
            )
        else:
            await self.exec_write_operation(
                """
                UPDATE currency
                SET coins = coins + %s
                WHERE user_id = %s
                """,
                (coins, user_id),
            )
