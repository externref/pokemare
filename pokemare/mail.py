import time

import disnake
from datetime import datetime
import uuid
import math


class Mail:
    def __init__(
            self,
            from_id: int = 0,
            to_id: int = 0,
            subject: str = "",
            message: str = "",
            mail_type: str = "standard",
            item=None,
            pokemon=None
    ):
        self.unique_id = uuid.uuid4()
        self.from_id = from_id
        self.to_id = to_id
        self.subject = subject
        self.message = message
        self.mail_type = mail_type
        self.item = item
        self.pokemon = pokemon
        self.timestamp = datetime.today()
        self.read = False

    def has_attachments(self):
        if self.item or self.pokemon:
            return True
        return False

    def receive_all_attachments(self):
        self.receive_item()
        self.receive_pokemon()

    def receive_item(self):
        if self.item:
            # TODO: Give item to user
            pass
        self.item = None

    def receive_pokemon(self):
        if self.pokemon:
            # TODO: Give Pokemon to user
            pass
        self.pokemon = None

    def add_item(self, item):
        self.item = item

    def add_pokemon(self, pokemon):
        self.pokemon = pokemon


class MailBox:
    def __init__(self, user_identifier: int):
        self.mail_dict = {}
        self.user_identifier = user_identifier
        self.unread = 0
        self.items_waiting = 0
        self.pokemon_waiting = 0

    def add_mail(self, mail: Mail):
        self.mail_dict[mail.unique_id] = mail

    def delete_mail(self, unique_id):
        if unique_id in self.mail_dict.keys():
            del self.mail_dict[unique_id]

    def mark_mail_as_read(self, mail):
        if mail.unique_id in self.mail_dict.keys():
            self.mail_dict[mail.unique_id].read = True

    def claim_mail_attachments(self, mail):
        if mail.unique_id in self.mail_dict.keys():
            self.mail_dict[mail.unique_id].receive_all_attachments()

    def sort_mailbox_by_date(self):
        mail_list = list(self.mail_dict.values())
        mail_list.sort(key=lambda m: m.timestamp, reverse=True)
        mail_list.sort(key=lambda m: m.read)
        return mail_list

    def receive_item(self, unique_id):
        if unique_id in self.mail_dict.keys():
            self.mail_dict[unique_id].receive_item()

    def receive_pokemon(self, unique_id):
        if unique_id in self.mail_dict.keys():
            self.mail_dict[unique_id].receive_pokemon()

    def update_fields(self):
        self.unread = 0
        self.items_waiting = 0
        self.pokemon_waiting = 0
        for mail in list(self.mail_dict.values()):
            if not mail.read:
                self.unread += 1
            if mail.item:
                self.items_waiting += 1
            if mail.pokemon:
                self.pokemon_waiting += 1


class MailHomeEmbed(disnake.embeds.Embed):
    def __init__(self, mailbox: MailBox, user):
        mailbox.update_fields()
        super().__init__(title="Welcome to your PokéMare Mailbox!",
                         description=":mailbox_with_mail:・Unread Messages: " + str(mailbox.unread) + "\n"
                                                                                                     "<:potion:941956192010371073>・Unclaimed Items: " + str(
                             mailbox.items_waiting) + "\n"
                                                      "<:POKEMON:942110736577077268>・Unclaimed Pokemon: " + str(
                             mailbox.pokemon_waiting) + "\n\n\n"
                                                        ":mailbox:・Click 'Inbox' below to view your inbox.\n"
                                                        ":incoming_envelope:・Click 'Send' below to send a new mail.\n"
                         )
        self.user = user
        self.init_footer()
        self.init_thumbnail()
        self.color = disnake.Color.blue()

    def init_footer(self):
        self.set_footer(
            text=f"MailBox for {self.user}",
            icon_url=self.user.display_avatar,
        )

    def init_thumbnail(self):
        self.set_thumbnail(
            url="https://i.imgur.com/BR7T4zp.png"
        )


class InboxEmbed(disnake.embeds.Embed):
    def __init__(self, mailbox: MailBox, user, page_offset=0):
        mailbox.update_fields()
        super().__init__(title="PokéMare Inbox (pg." + str(page_offset + 1) + ")",
                         description=(":mailbox_with_mail:・Unread Messages: " + str(mailbox.unread)
                                      + "\n-------------------------------------"))
        self.user = user
        self.init_footer()
        self.init_thumbnail()
        self.page_offset = page_offset
        self.mail_list = mailbox.sort_mailbox_by_date()
        self.color = disnake.Color.blue()
        self.init_fields()

    def init_fields(self):
        emoji_list = [":one:", ":two:", ":three:", ":four:", ":five:"]
        for x in range(5):
            index = x + self.page_offset * 5
            if index < len(self.mail_list):
                mail = self.mail_list[index]
                subject_unread = ""
                if not mail.read:
                    subject_unread = " ✉️"
                value_str = "*From*: " + str(mail.from_id) + "\n*Message preview:*\n" + mail.message[:100] + "..."
                value_str_append = ""
                if mail.has_attachments():
                    value_str_append = "Att: "
                    if mail.pokemon:
                        value_str_append += "<:POKEMON:942110736577077268>"
                    if mail.item:
                        value_str_append += "<:potion:941956192010371073>"
                    value_str_append += "\n"
                value_str = value_str_append + value_str
                value_str += "\n\n-------------------------------------"
                self.add_field(name=emoji_list[x] + " SUBJECT: " + mail.subject + subject_unread,
                               value=value_str,
                               inline=False
                               )
            else:
                self.add_field(name=emoji_list[x] + " - Empty mail slot" + "\n\n----------------------"
                               , value="\u200b", inline=False)

    def init_footer(self):
        self.set_footer(
            text=f"MailBox for {self.user}",
            icon_url=self.user.display_avatar,
        )

    def init_thumbnail(self):
        self.set_thumbnail(
            url="https://i.imgur.com/BR7T4zp.png"
        )


class MailReadEmbed(disnake.embeds.Embed):
    def __init__(self, mailbox: MailBox, user, mail):
        # TODO: Make attachments more specific once we have items and Pokemon implemented
        attachment_str = ""
        if mail.has_attachments():
            attachment_str = "*ATTACHMENTS*: "
            if mail.pokemon:
                attachment_str += "<:POKEMON:942110736577077268>"
            if mail.item:
                attachment_str += "<:potion:941956192010371073>"
            attachment_str += "\n"
        # TODO: Replace from_id with user name using database or trainer class or whatever
        description_str = "*FROM:* " + str(mail.from_id) + "\n" + attachment_str + "\n"
        super().__init__(title="SUBJECT: " + mail.subject,
                         description=description_str)
        self.user = user
        self.init_footer()
        self.init_thumbnail()
        self.init_fields(mail)
        self.color = disnake.Color.blue()
        mailbox.mark_mail_as_read(mail)

    def init_footer(self):
        self.set_footer(
            text=f"MailBox for {self.user}",
            icon_url=self.user.display_avatar,
        )

    def init_thumbnail(self):
        # TODO: Make thumbnail the type of mail (ie. dive mail, sky mail, etc)
        self.set_thumbnail(
            url="https://i.imgur.com/BR7T4zp.png"
        )

    def init_fields(self, mail):
        self.add_field(name="\u200b",
                       value=mail.message[:1024])


class MailReadView(disnake.ui.View):
    def __init__(self, mailbox, user, mail, page_offset, bot):
        super().__init__()
        self.mailbox = mailbox
        self.mail = mail
        self.user = user
        self.page_offset = page_offset
        self.bot = bot
        self.update_buttons()

    def update_buttons(self):
        if not self.mail.has_attachments():
            self.children[1].disabled = True
            self.children[2].disabled = False
        else:
            self.children[1].disabled = False
            self.children[2].disabled = True

    @disnake.ui.button(label="Reply", style=disnake.ButtonStyle.grey, emoji="📨")
    async def reply_button_press(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if not await verify_author(interaction, self.user):
            return
        await interaction.response.send_modal(modal=SendModal(self.mailbox, self.bot, self.mail.from_id))

    @disnake.ui.button(label="Claim all attachments", style=disnake.ButtonStyle.grey)
    async def claim_button_press(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if not await verify_author(interaction, self.user):
            return
        if self.mail.has_attachments():
            self.mailbox.claim_mail_attachments(self.mail)
            self.update_buttons()
            embed = MailReadEmbed(self.mailbox, self.user, self.mail)
            view = MailReadView(self.mailbox, self.user, self.mail, self.page_offset, self.bot)
            await interaction.response.edit_message(embed=embed, view=view)
        else:
            await interaction.response.defer()

    @disnake.ui.button(label="Delete", style=disnake.ButtonStyle.grey, emoji="❌")
    async def delete_button_press(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if not await verify_author(interaction, self.user):
            return
        self.mailbox.delete_mail(self.mail.unique_id)
        embed = InboxEmbed(self.mailbox, self.user, self.page_offset)
        view = InboxView(self.mailbox, self.user, self.page_offset, self.bot)
        await interaction.response.edit_message(embed=embed, view=view)

    @disnake.ui.button(label="Inbox", style=disnake.ButtonStyle.grey, emoji="↩️")
    async def back_button_press(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if not await verify_author(interaction, self.user):
            return
        embed = InboxEmbed(self.mailbox, self.user, self.page_offset)
        view = InboxView(self.mailbox, self.user, self.page_offset, self.bot)
        await interaction.response.edit_message(embed=embed, view=view)


class InboxView(disnake.ui.View):
    def __init__(self, mailbox, user, page_offset, bot):
        super().__init__()
        self.mailbox = mailbox
        self.user = user
        self.page_offset = page_offset
        self.bot = bot
        self.max_pages = math.ceil(len(self.mailbox.sort_mailbox_by_date()) / 5)
        self.update_buttons()

    def update_buttons(self):
        for x in range(5):
            index = x + self.page_offset * 5
            if index < len(self.mailbox.sort_mailbox_by_date()):
                self.children[x].disabled = False
            else:
                self.children[x].disabled = True


    @disnake.ui.button(label="\u200b", style=disnake.ButtonStyle.grey, emoji="1️⃣")
    async def one_button_press(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self.read_mail(1, interaction)

    @disnake.ui.button(label="\u200b", style=disnake.ButtonStyle.grey, emoji="2️⃣")
    async def two_button_press(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self.read_mail(2, interaction)

    @disnake.ui.button(label="\u200b", style=disnake.ButtonStyle.grey, emoji="3️⃣")
    async def three_button_press(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self.read_mail(3, interaction)

    @disnake.ui.button(label="\u200b", style=disnake.ButtonStyle.grey, emoji="4️⃣")
    async def four_button_press(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self.read_mail(4, interaction)

    @disnake.ui.button(label="\u200b", style=disnake.ButtonStyle.grey, emoji="5️⃣")
    async def five_button_press(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self.read_mail(5, interaction)

    @disnake.ui.button(label="\u200b", style=disnake.ButtonStyle.grey, emoji="⬅️")
    async def left_button_press(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if not await verify_author(interaction, self.user):
            return
        self.page_offset -= 1
        if self.page_offset < 0:
            self.page_offset = self.max_pages - 1
        embed = InboxEmbed(self.mailbox, self.user, self.page_offset)
        self.update_buttons()
        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(label="\u200b", style=disnake.ButtonStyle.grey, emoji="➡️")
    async def right_button_press(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if not await verify_author(interaction, self.user):
            return
        self.page_offset += 1
        if self.page_offset > self.max_pages - 1:
            self.page_offset = 0
        embed = InboxEmbed(self.mailbox, self.user, self.page_offset)
        self.update_buttons()
        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(label="Home", style=disnake.ButtonStyle.grey, emoji="↩️")
    async def back_button_press(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if not await verify_author(interaction, self.user):
            return
        embed = MailHomeEmbed(self.mailbox, self.user)
        view = MailHomeView(self.mailbox, self.user, self.bot)
        await interaction.response.edit_message(embed=embed, view=view)

    async def read_mail(self, button_number, interaction):
        if not await verify_author(interaction, self.user):
            return
        index = button_number - 1 + self.page_offset * 5
        mail = self.mailbox.sort_mailbox_by_date()[index]
        embed = MailReadEmbed(self.mailbox, self.user, mail)
        view = MailReadView(self.mailbox, self.user, mail, self.page_offset, self.bot)
        await interaction.response.edit_message(embed=embed, view=view)


class MailHomeView(disnake.ui.View):
    def __init__(self, mailbox: MailBox, user, bot):
        super().__init__()
        self.mailbox = mailbox
        self.user = user
        self.bot = bot

    @disnake.ui.button(label="Inbox", style=disnake.ButtonStyle.grey, emoji="📫")
    async def inbox_button_press(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if not await verify_author(interaction, self.user):
            return
        embed = InboxEmbed(self.mailbox, self.user, 0)
        view = InboxView(self.mailbox, self.user, 0, self.bot)
        await interaction.response.edit_message(embed=embed, view=view)

    @disnake.ui.button(label="Send New Mail", style=disnake.ButtonStyle.grey, emoji="📨")
    async def send_button_press(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if not await verify_author(interaction, self.user):
            return
        await interaction.response.send_modal(modal=SendModal(self.mailbox, self.bot))


# Subclassing the modal.
class SendModal(disnake.ui.Modal):
    def __init__(self, mailbox: MailBox, bot, to: int = 0):
        # TODO: Support attachments of items and Pokemon
        # TODO: Remove temporary testing dict
        global mailbox_dict
        self.mailbox = mailbox
        self.bot = bot
        components = []
        if to == 0:
            components.append(disnake.ui.TextInput(
                label="To:",
                placeholder="Enter the Discord name or ID.",
                custom_id="to",
                style=disnake.TextInputStyle.short,
                max_length=50,
            ))
        else:
            components.append(disnake.ui.TextInput(
                label="To:",
                value=str(to),
                custom_id="to",
                style=disnake.TextInputStyle.short,
                max_length=50,
            ))
        components.append(disnake.ui.TextInput(
            label="Subject",
            placeholder="Enter the subject line of your message here.",
            custom_id="subject",
            style=disnake.TextInputStyle.short,
            max_length=50,
        ))
        components.append(disnake.ui.TextInput(
            label="Message",
            placeholder="Enter your message here.",
            custom_id="message",
            style=disnake.TextInputStyle.paragraph,
            max_length=1000,
        ))
        super().__init__(
            title="Send a New Message",
            custom_id="send_message",
            components=components,
        )

    async def callback(self, inter: disnake.ModalInteraction):
        # Todo update with actual database of users, will need to fetch user and their mailbox
        embed = disnake.Embed(title="Message sent!")
        to = int(inter.text_values["to"])
        subject = inter.text_values["subject"]
        message = inter.text_values["message"]
        new_mail = Mail(self.mailbox.user_identifier,
                        to,
                        subject,
                        message)
        if to in mailbox_dict.keys():
            to_mailbox = mailbox_dict[to]
            to_mailbox.add_mail(new_mail)
            user = self.bot.get_user(to)
            try:
                await user.send("You have new mail! View it in your mailbox now with `/mail`!")
            except:
                pass
            for key, value in inter.text_values.items():
                embed.add_field(
                    name=key.capitalize(),
                    value=value[:1024],
                    inline=False,
                )
            await inter.response.send_message(embed=embed, ephemeral=True)
        else:
            await inter.response.send_message("User not apart of beta mail group.")


async def verify_author(interaction, user):
    if interaction.author != user:
        await interaction.response.send_message(
            "Sorry this mailbox is for: "
            + user.name
            + "\nPlease request your own mailbox with `/mail`!",
            ephemeral=True,
        )
        return False
    return True


# TODO: Test setup removal
zetaroid_mailbox = MailBox(189312357892096000)
new_mail = Mail(189312357892096000, 189312357892096000, "Subject 1", "Test mail 1")
time.sleep(2)
new_mail_2 = Mail(189312357892096000, 189312357892096000, "Subject 2", "Test mail 2")
new_mail_2.add_item("TEST ITEM")
time.sleep(2)
new_mail_3 = Mail(189312357892096000, 189312357892096000, "Subject 3", "Test mail 3")
time.sleep(2)
new_mail_4 = Mail(189312357892096000, 189312357892096000, "Subject 4", "Test mail 4")
new_mail_4.add_pokemon("TEST POKEMON")
time.sleep(2)
new_mail_5 = Mail(189312357892096000, 189312357892096000, "Subject 5", "Test mail 5")
time.sleep(2)
new_mail_6 = Mail(189312357892096000, 189312357892096000, "Subject 6", "Test mail 6")
new_mail_6.add_item("TEST ITEM")
new_mail_6.add_pokemon("TEST POKEMON")
zetaroid_mailbox.add_mail(new_mail_3)
zetaroid_mailbox.add_mail(new_mail)
zetaroid_mailbox.add_mail(new_mail_5)
zetaroid_mailbox.add_mail(new_mail_6)
zetaroid_mailbox.add_mail(new_mail_4)
zetaroid_mailbox.add_mail(new_mail_2)
mailbox_dict = {580034015759826944: MailBox(580034015759826944),
                189312357892096000: zetaroid_mailbox,
                775243228311191572: MailBox(775243228311191572),
                735830204286763148: MailBox(735830204286763148),
                928979024812867614: MailBox(928979024812867614),
                716840809353314344: MailBox(716840809353314344),
                404418440187740171: MailBox(404418440187740171),
                710910223698624513: MailBox(710910223698624513),
                942293716410982462: MailBox(942293716410982462),
                533591507744325642: MailBox(533591507744325642),
                246135956007157762: MailBox(246135956007157762),
                311977451116822540: MailBox(311977451116822540)}
