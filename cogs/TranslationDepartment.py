import disnake
from disnake.ext import commands

import datetime
import json
import os

config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

with open(config_path) as config:
    config = json.load(config)

channel = config['channels']['TranslationDepartment']
highstaff = config['roles']['HighStaff']


class TranslationDepartment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def перевод(self, inter, будущий_отдел: disnake.Role):
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
            departments = config['roles']['departments'].values()
            department = ""
            for role in inter.author.roles:
                if role.id in departments:
                    department = str(role.id)
                    break
            if department == "":
                department = "Не определён"
            embed = disnake.Embed(
                title="Заявление на перевод",
                color = 0x2B2D31,
                timestamp=datetime.datetime.now()
            )
            if будущий_отдел.id in departments:
                embed.add_field(name="Нынешний отдел:", value=f"<@&{department}>")
                embed.add_field(name="Будущий отдел:", value=f"{будущий_отдел.mention}")
                channelObj = disnake.utils.get(inter.guild.channels, id=channel)
                await channelObj.send(f"<@&{highstaff}> рассмотрите запрос от {inter.author.mention}",embed=embed, components=[
                        disnake.ui.Button(label="Одобрить", style=disnake.ButtonStyle.success, custom_id="Approve"),
                        disnake.ui.Button(label="Отклонить", style=disnake.ButtonStyle.danger, custom_id="Reject")
                    ],)
                await inter.send("**🟢 Вы успешно отправили запрос!**", ephemeral=True)
            else:
                error_embed = disnake.Embed(
                    title="Ошибка",
                    description="Разрешено указывать только роли отделов",
                    color = 0xDA373C,
                    timestamp=datetime.datetime.now()
                )
                text = ""
                for role in departments:
                    text = text + "\n<@&" + str(role) +">"
                error_embed.add_field(name="Разрешённые роли:", value=f"{text}")
                await inter.response.send_message(ephemeral=True, embed=error_embed)




def setup(bot: commands.Bot):
    bot.add_cog(TranslationDepartment(bot))
