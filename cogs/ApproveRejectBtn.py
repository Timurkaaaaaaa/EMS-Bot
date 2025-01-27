import datetime
import disnake
from disnake.ext import commands

import datetime
import json
import os

config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

with open(config_path) as config:
    config = json.load(config)

highstaff = config['roles']['HighStaff']
HeadPhysician = config['roles']['HeadPhysician']
DeputyHeadPhysician = config['roles']['DeputyHeadPhysician']

channel = config['channels']['DefibrillatorReport']

with open("config.json") as config:
    config = json.load(config)

class ApproveRejectBtnLogic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.highstaff_role_id = highstaff  # Замените на ID роли HighStaff

    @commands.Cog.listener("on_button_click")
    async def ApproveRejectBtnLogic(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id not in ["Approve", "Reject"]:
            return

        highstaff_role = disnake.utils.get(inter.guild.roles, id=self.highstaff_role_id)
        message_text = inter.message.content
        index = message_text.rfind("<")
        message_author = message_text[index + 2:-1]

        if highstaff_role not in inter.author.roles:
            emb = disnake.Embed(
                title="Ошибка",
                description="Вы не можете рассматривать отчёт!",
                color=0xDA373C,
                timestamp=datetime.datetime.now()
            )
            await inter.response.send_message(embed=emb, ephemeral=True)
            return

        if inter.component.custom_id == "Approve":
            new_message_text = f"<@{inter.author.id}> одобрил заявление от <@{message_author}>"
            await inter.response.edit_message(
                content=new_message_text,
                components=[
                    disnake.ui.Button(label="Одобрено", disabled=True, style=disnake.ButtonStyle.success),
                    disnake.ui.Button(label="Аннулировать", style=disnake.ButtonStyle.secondary, custom_id="Cancel")
                ]
            )
        elif inter.component.custom_id == "Reject":
            new_message_text = f"<@{inter.author.id}> отклонил заявление от <@{message_author}>"
            await inter.response.edit_message(
                content=new_message_text,
                components=[
                    disnake.ui.Button(label="Отклонено", disabled=True, style=disnake.ButtonStyle.danger),
                    disnake.ui.Button(label="Аннулировать", style=disnake.ButtonStyle.secondary, custom_id="Cancel")
                ]
            )


class CancelBtnLogic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.highstaff_role_id = highstaff  # Замените на ID роли HighStaff

    @commands.Cog.listener("on_button_click")
    async def CancelBtnLogic(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id != "Cancel":
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
                disnake.ui.Button(label="Одобрить", style=disnake.ButtonStyle.success, custom_id="Approve"),
                disnake.ui.Button(label="Отклонить", style=disnake.ButtonStyle.danger, custom_id="Reject")
            ]
        )

# Регистрация cog-ов
def setup(bot):
    bot.add_cog(ApproveRejectBtnLogic(bot))
    bot.add_cog(CancelBtnLogic(bot))