import datetime
import disnake
from disnake.ext import commands
from disnake import TextInputStyle

import datetime
import json
import os

import sqlite3


connection = sqlite3.connect('Defibrillator.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS DefibrillatorReport (
received INTEGER,
issued INTEGER,
link TEXT
)
''')

connection.commit()

config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

with open(config_path) as config:
    config = json.load(config)

channel = config['channels']['DefibrillatorReport']
highstaff = config['roles']['HighStaff']
HeadPhysician = config['roles']['HeadPhysician']
DeputyHeadPhysician = config['roles']['DeputyHeadPhysician']

class DefibrillatorReportModal(disnake.ui.Modal):
    def __init__(self):
        # Детали модального окна и его компонентов
        components = [
            disnake.ui.TextInput(
                label="Номер дефибриллятора",
                placeholder="Пример: EMS-ABC12345-123456",
                custom_id="Номер дефибриллятора:",
                style=TextInputStyle.short,
                max_length=100,
            ),
            disnake.ui.TextInput(
                label="Ссылка на изображение",
                placeholder="Изображение с инвентарём",
                custom_id="Ссылка на изображение:",
                style=TextInputStyle.short,
                max_length=1024,
            )
        ]
        super().__init__(
            title="Отчёт о выдаче дефибриллятора",
            custom_id="DefibrillatorReportModal",
            components=components,
        )

    # Обработка ответа, после отправки модального окна
    async def callback(self, inter: disnake.ModalInteraction):
        embed = disnake.Embed(
            title="Отчёт по выдаче",
            color=0x2B2D31
        )

        cursor.execute('SELECT received, link FROM DefibrillatorReport WHERE issued = ?', (inter.author.id,))
        data = cursor.fetchall()
        cursor.execute('DELETE FROM DefibrillatorReport WHERE issued = ?', (inter.author.id,))

        recieved = data[0][0]
        link = data[0][1]

        embed.add_field(
                name="Сотрудник выдавший:",
                value=f"{inter.author.mention}",
                inline=True,
            )
        embed.add_field(
                name="Сотрудник получивший:",
                value=f"<@&{recieved}>",
                inline=True,
            )
        embed.add_field(
                name="Запрос на получение:",
                value=f"{link}",
                inline=True,
            )
        embed.add_field(
                name="Действие:",
                value="Выдал",
                inline=False,
            )
        for key, value in inter.text_values.items():
            embed.add_field(
                name=key.capitalize(),
                value=value[:1024],
                inline=False,
            )
        channelObj = disnake.utils.get(inter.guild.channels, id=channel)
        await channelObj.send(embed=embed)
        await inter.send("**🟢 Вы успешно отправили отчёт!**", ephemeral=True)


class DefibrillatorApproveRejectBtnLogic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.highstaff_role_id = highstaff  # Замените на ID роли HighStaff

    @commands.Cog.listener("on_button_click")
    async def DefibrillatorApproveRejectBtnLogic(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id not in ["DefibrillatorApprove", "DefibrillatorReject"]:
            return

        highstaff_role = disnake.utils.get(inter.guild.roles, id=self.highstaff_role_id)
        message_text = inter.message.content
        index = message_text.rfind("<")
        message_author = message_text[index + 2:-1]

        if highstaff_role not in inter.author.roles:
            emb = disnake.Embed(
                title="Ошибка",
                description="Вы не можете рассматривать заявления!",
                color=0xDA373C,
                timestamp=datetime.datetime.now()
            )
            await inter.response.send_message(embed=emb, ephemeral=True)
            return

        if inter.component.custom_id == "DefibrillatorApprove":
            #create link:
            discordid = config["discordServerID"]
            link = "https://discord.com/channels/" + str(discordid) + "/" + str(channel) + "/" + str(inter.message.id)
            cursor.execute('INSERT INTO DefibrillatorReport (received, issued, link) VALUES (?, ?, ?)', (message_author, inter.author.id, link))
            await inter.response.send_modal(modal=DefibrillatorReportModal())

            new_message_text = f"<@{inter.author.id}> одобрил заявление от <@{message_author}>"
            await inter.followup.edit_message(
                inter.message.id,
                content=new_message_text,
                components=[
                    disnake.ui.Button(label="Одобрено", disabled=True, style=disnake.ButtonStyle.success),
                    disnake.ui.Button(label="Аннулировать", style=disnake.ButtonStyle.secondary, custom_id="DefibrillatorCancel")
                ]
            )
        elif inter.component.custom_id == "DefibrillatorReject":
            new_message_text = f"<@{inter.author.id}> отклонил заявление от <@{message_author}>"
            await inter.response.edit_message(
                content=new_message_text,
                components=[
                    disnake.ui.Button(label="Отклонено", disabled=True, style=disnake.ButtonStyle.danger),
                    disnake.ui.Button(label="Аннулировать", style=disnake.ButtonStyle.secondary, custom_id="DefibrillatorCancel")
                ]
            )


class DefibrillatorCancelBtnLogic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.highstaff_role_id = highstaff  # Замените на ID роли HighStaff

    @commands.Cog.listener("on_button_click")
    async def DefibrillatorCancelBtnLogic(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id != "DefibrillatorCancel":
            return

        highstaff_role = disnake.utils.get(inter.guild.roles, id=self.highstaff_role_id)

        if highstaff_role not in inter.author.roles:
            emb_error = disnake.Embed(
                title="Ошибка",
                description="Вы не можете аннулировать решение старшего состава",
                color=0xDA373C,
                timestamp=datetime.datetime.now()
            )
            await inter.response.send_message(embed=emb_error, ephemeral=True)
            return

        message_text = inter.message.content
        index = message_text.rfind("<")
        new_message_text = f"<@&{self.highstaff_role_id}> рассмотрите заявление от {message_text[index:]}"
        await inter.response.edit_message(
            content=new_message_text,
            components=[
                disnake.ui.Button(label="Одобрить", style=disnake.ButtonStyle.success, custom_id="DefibrillatorApprove"),
                disnake.ui.Button(label="Отклонить", style=disnake.ButtonStyle.danger, custom_id="DefibrillatorReject")
            ]
        )

# Регистрация cog-ов
def setup(bot):
    bot.add_cog(DefibrillatorApproveRejectBtnLogic(bot))
    bot.add_cog(DefibrillatorCancelBtnLogic(bot))
