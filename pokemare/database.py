import aiosqlite
from typing import Optional, Tuple
from disnake.ext.commands.bot import Bot


class UserInfoDatabase:
    def __init__(self, database_file_path, bot: Bot):
        self.databse_file = database_file_path
        self.bot = bot

    async def create_and_connect(self):
        self.user_database: aiosqlite.Connection = await aiosqlite.connect(
            self.databse_file
        )
        await self.user_database.execute(
            """
            CREATE TABLE IF NOT EXISTS users
            (
                user_id TEXT,
                starter_id TEXT,
                badges TEXT,
                pokedollars TEXT,
                stars TEXT
            )
            """
        )
        await self.user_database.commit()

    async def get_user_information(self, user_id) -> Optional[Tuple]:
        async with self.user_database.cursor() as cursor:
            await cursor.execute(
                """
                SELECT * FROM users
                WHERE user_id = ?
                """,
                (user_id,),
            )
            return await cursor.fetchone()

    async def insert_user_into_database(self, user_id: str, starter_id: str) -> None:
        async with self.user_database.cursor() as cursor:
            await cursor.execute(
                """
                INSERT INTO users
                ( user_id ,  starter_id , badges,   pokedollars , stars )
                VALUES ( ? , ?, ? , ? , ?)
                """,
                (user_id, starter_id, "", "2500", "0"),
            )
            await self.user_database.commit()
