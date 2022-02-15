from json import load
from random import randint
from disnake.ext.commands.context import Context
import disnake


class TriviaInfo:
    def __init__(
        self,
        identifier=0,
        question="",
        answer="",
        question_type="",
        response="",
        options=None,
    ):
        self.identifier = identifier
        self.question = question
        self.answer = answer
        self.question_type = question_type
        self.response = response
        self.options = options


class TriviaList:
    def __init__(self):
        self.dict = {}
        self.filename = "trivia.json"

    def add_trivia(self, trivia: TriviaInfo, question_type):
        if question_type not in self.dict.keys():
            self.dict[question_type] = []
        self.dict[question_type].append(trivia)

    def get_random_trivia(self):
        type_selection_index = randint(0, len(self.dict.keys()) - 1)
        trivia_type = list(self.dict.keys())[type_selection_index]
        trivia_selection_index = randint(0, len(self.dict[trivia_type]) - 1)
        return self.dict[trivia_type][trivia_selection_index]

    def load_from_json(self, filename: str = ""):
        if not filename:
            filename = self.filename
        with open("data/" + filename, "r", encoding="utf8") as read_file:
            trivia_data = load(read_file)
        for trivia_type in trivia_data["trivia_question_types"]:
            for trivia_object in trivia_data["trivia_" + trivia_type.replace(" ", "_")]:
                options = []
                for option in trivia_object["options"]:
                    options.append(option)
                trivia = TriviaInfo(
                    trivia_object["id"],
                    trivia_object["question"],
                    trivia_object["answer"],
                    trivia_type,
                    trivia_object["response"],
                    options,
                )
                self.add_trivia(trivia, trivia_type)


class TriviaButtons(disnake.ui.View):
    def __init__(self, answer_index: str, author: Context.author):
        super().__init__()
        self.value = ""
        self.answer_index = answer_index
        self.author = author
        self.correct = False

    @disnake.ui.button(label="A", style=disnake.ButtonStyle.green)
    async def option_a(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        await self.verify_response("A", interaction)

    @disnake.ui.button(label="B", style=disnake.ButtonStyle.green)
    async def option_b(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        await self.verify_response("B", interaction)

    @disnake.ui.button(label="C", style=disnake.ButtonStyle.green)
    async def option_c(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        await self.verify_response("C", interaction)

    @disnake.ui.button(label="D", style=disnake.ButtonStyle.green)
    async def option_d(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        await self.verify_response("D", interaction)

    async def verify_response(self, value, interaction: disnake.MessageInteraction):
        if interaction.author != self.author:
            await interaction.response.send_message(
                "Sorry this trivia is for: "
                + self.author.name
                + "\nPlease request your own trivia!",
                ephemeral=True,
            )
            return
        self.value = value
        number = ord(self.value) - 65
        if number == self.answer_index:
            self.correct = True
        await interaction.response.defer()
        self.stop()
