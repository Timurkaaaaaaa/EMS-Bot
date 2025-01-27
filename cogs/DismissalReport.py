import disnake
from disnake.ext import commands
from disnake import TextInputStyle

import datetime
import json
import os

config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

with open(config_path) as config:
    config = json.load(config)

channel = config['channels']['DismissalReport']
highstaff = config['roles']['HighStaff']


class DismissalReport(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def заявление_на_увольнение(self, inter):
        channel_id = inter.channel.id
        if channel_id != channel:
            error_emb = disnake.Embed(
                title="Ошибка",
                description=f"Данную команду можно использовать только в <#{channel}>",
                color = 0xDA373C,
                timestamp=datetime.datetime.now()
            )
            await inter.response.send_message(embed=error_emb, ephemeral=True)
        else:
            emb = disnake.Embed(
                title="Заявление на увольнение",
                color = 0xE74D3C,
                timestamp=datetime.datetime.now()
            )
            await inter.response.send_modal(modal=DismissalReportModal())
            await inter.response.send_message(embed=emb, ephemeral=True)




def setup(bot: commands.Bot):
    bot.add_cog(DismissalReport(bot))

class DismissalReportModal(disnake.ui.Modal):
    def __init__(self):
        # Детали модального окна и его компонентов
        components = [
            disnake.ui.TextInput(
                label="Ранг",
                placeholder="Пример: 13 ранг",
                custom_id="Ранг:",
                style=TextInputStyle.short,
                max_length=2,
            ),
            disnake.ui.TextInput(
                label="Отдел",
                placeholder="Пример: PSID",
                custom_id="Отдел:",
                style=TextInputStyle.short,
                max_length=5,
            ),
            disnake.ui.TextInput(
                label="Скриншот инвентаря:",
                placeholder="https://example.com/",
                custom_id="Скриншот инвентаря:",
                style=TextInputStyle.short,
                max_length=150,
            ),
            disnake.ui.TextInput(
                label="Сдача дефибриллятора:",
                placeholder="https://example.com/",
                custom_id="Сдача дефибриллятора:",
                style=TextInputStyle.short,
                max_length=150,
            ),
            disnake.ui.TextInput(
                label="Причина увольнения:",
                placeholder="Пример: по собственному желанию",
                custom_id="Причина увольнения:",
                style=TextInputStyle.paragraph,
                max_length=1024,
            ),
        ]
        super().__init__(
            title="Заявление на увольнение",
            custom_id="DismissalReportModal",
            components=components,
        )

    # Обработка ответа, после отправки модального окна
    async def callback(self, inter: disnake.ModalInteraction):
        embed = disnake.Embed(
            title="Заявление на увольнение",
            color=0xE74D3C
        )
        for key, value in inter.text_values.items():
            embed.add_field(
                name=key.capitalize(),
                value=value[:1024],
                inline=False,
            )
        channelObj = disnake.utils.get(inter.guild.channels, id=channel)
        await channelObj.send(f"<@&{highstaff}> рассмотрите заявление от {inter.author.mention}",embed=embed, components=[
                disnake.ui.Button(label="Одобрить", style=disnake.ButtonStyle.success, custom_id="Approve"),
                disnake.ui.Button(label="Отклонить", style=disnake.ButtonStyle.danger, custom_id="Reject")
            ],)
        await inter.send("**🟢 Вы успешно отправили заявление!**", ephemeral=True)