from pokemare import PokeMare
from os import getenv

if __name__ == "__main__":
    PokeMare(getenv("BOT_TOKEN")).run()
