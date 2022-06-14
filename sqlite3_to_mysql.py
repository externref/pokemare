import sqlite3, os, aiomysql, asyncio


db = sqlite3.connect("gtpdatabase.db")
cursor = db.cursor()
cursor.execute("SELECT * FROM guesses")
data = cursor.fetchall()
print(data)


async def main():
    database: aiomysql.Connection = await aiomysql.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        db=os.getenv("MYSQLDATABASE"),
        password=os.getenv("MYSQLPASSWORD"),
        port=int(os.getenv("MYSQLPORT")),
        loop=asyncio.get_event_loop(),
        autocommit=False,
    )

    cursor: aiomysql.Cursor = await database.cursor()
    await cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS guesses
        ( user_id BIGINT, guild_id BIGINT, guesses INT ) ;
        """
    )
    await database.commit()
    for values in data:
        await cursor.execute("INSERT INTO guesses VALUES ( %s, %s, %s)", values)
    await database.commit()
    database.close()


asyncio.run(main())
