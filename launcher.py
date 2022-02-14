from pokemare import PokeMare
from dotenv import load_dotenv
from os import getenv

if __name__ == "__main__":
    load_dotenv()
    PokeMare(getenv("BOT_TOKEN")).run()
