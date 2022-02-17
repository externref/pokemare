import aiosqlite
from typing import Optional, Tuple
from disnake.ext.commands.bot import Bot

from pokemare.mail import MailBox
from pokemare.user import User


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
                name TEXT,
                starter_id TEXT,
                badges TEXT,
                pokedollars TEXT,
                stars TEXT,
                mailbox TEXT
            )
            """
        )
        await self.user_database.commit()

    async def get_user(self, user_id):
        user = User(self.bot)
        data = await self.get_user_information(user_id)
        if data:
            user.load_from_data(data)
            return user
        return None

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

    async def insert_user_into_database(self, user_id: str, author_name: str, name: str, starter_id: str) -> None:
        async with self.user_database.cursor() as cursor:
            await cursor.execute(
                """
                INSERT INTO users
                ( user_id, name, starter_id, badges, pokedollars, stars, mailbox )
                VALUES ( ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (user_id, name, starter_id, "", "2500", "0", MailBox(int(user_id)).to_string()),
            )
            await self.user_database.commit()

    async def update_user_name(self, user_id: str, name: str):
        async with self.user_database.cursor() as cursor:
            await cursor.execute(
                """
                UPDATE users
                SET name = ?
                WHERE user_id = ?
                """,
                (name, user_id),
            )
            await self.user_database.commit()

    async def update_user_mailbox(self, user_id: str, mailbox_string: str):
        async with self.user_database.cursor() as cursor:
            await cursor.execute(
                """
                UPDATE users
                SET mailbox = ?
                WHERE user_id = ?
                """,
                (mailbox_string, user_id),
            )
            await self.user_database.commit()

