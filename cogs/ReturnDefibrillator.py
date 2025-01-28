import disnake
from disnake.ext import commands
from disnake import TextInputStyle

import datetime
import json
import os


config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

with open(config_path) as config:
    config = json.load(config)

channel = config['channels']['DefibrillatorReport']
highstaff = config['roles']['HighStaff']

class DefibrillatorReturnModal(disnake.ui.Modal):
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
            title="Отчёт о сдаче дефибриллятора",
            custom_id="DefibrillatorReturnModal",
            components=components,
        )

    # Обработка ответа, после отправки модального окна
    async def callback(self, inter: disnake.ModalInteraction):
        embed = disnake.Embed(
            title="Отчёт по сдаче",
            color=0x2B2D31
        )

        embed.add_field(
                name="Сотрудник:",
                value=f"{inter.author.mention}",
                inline=True,
            )
        embed.add_field(
                name="Действие:",
                value="Сдал",
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



class ReturnDefibrillator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def сдать_дефибриллятор(self, inter):
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
            await inter.response.send_modal(modal=DefibrillatorReturnModal())
            await inter.send("**🟢 Вы успешно отправили запрос!**", ephemeral=True)



def setup(bot: commands.Bot):
    bot.add_cog(ReturnDefibrillator(bot))
