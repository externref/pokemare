from pokemare.mail import MailBox


class User(object):
    def __init__(self, bot):
        self.bot = bot
        self.identifier = 0
        self.name = ""
        self.starter_id = 0
        self.badges = []
        self.pokedollars = 0
        self.stars = 0
        self.mailbox = MailBox()

    def __copy__(self):
        pass

    def load_from_data(self, data):
        self.identifier = data[0]
        self.name = data[1]
        self.starter_id = data[2]
        self.badges = data[3]
        self.pokedollars = data[4]
        self.stars = data[5]
        self.mailbox = MailBox()
        self.mailbox.from_string(data[6])

    async def refresh_data(self):
        data = await self.bot.user_database.get_user_information(self.identifier)
        if data:
            self.load_from_data(data)

    async def delete_mail(self, mail):
        self.mailbox.delete_mail(mail)
        await self.bot.user_database.update_user_mailbox(self.identifier, self.mailbox.to_string())

    async def claim_all_mail_attachments(self, mail):
        self.mailbox.claim_mail_attachments(mail)
        await self.bot.user_database.update_user_mailbox(self.identifier, self.mailbox.to_string())

    async def mark_mail_as_read(self, mail):
        self.mailbox.mark_mail_as_read(mail)
        await self.bot.user_database.update_user_mailbox(self.identifier, self.mailbox.to_string())

    async def update_mailbox_fields(self):
        self.mailbox.update_fields()
        await self.bot.user_database.update_user_mailbox(self.identifier, self.mailbox.to_string())

    async def receive_mail(self, mail):
        self.mailbox.add_mail(mail)
        await self.bot.user_database.update_user_mailbox(self.identifier, self.mailbox.to_string())


