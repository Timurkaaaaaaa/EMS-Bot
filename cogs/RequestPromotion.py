import disnake
from disnake.ext import commands
import datetime
import json
import os

config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

with open(config_path) as config:
    config = json.load(config)

channel = config['channels']['RequestPromotion']
highstaff = config['roles']['HighStaff']


class RequestPromotion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def запрос_на_повышение(self, inter, повышаемый: disnake.Member, нынешний_ранг: int, будущий_ранг: int, кадровый_аудит: str, *, примечание: str = ""):
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
            if disnake.utils.get(inter.guild.roles, id=highstaff) in inter.author.roles:
                emb = disnake.Embed(
                    title="Запрос на повышение",
                    color = 0x2B2D31,
                    timestamp=datetime.datetime.now()
                )
                emb.add_field(name="Повышаемый:", value=f"{повышаемый.mention}", inline=False)
                emb.add_field(name="Нынешний ранг:", value=f"{нынешний_ранг}", inline=True)
                emb.add_field(name="Будущий ранг:", value=f"{будущий_ранг}", inline=True)
                emb.add_field(name="Кадровый аудит:", value=f"{кадровый_аудит}", inline=True)
                if примечание != "":
                    emb.add_field(name="Примечание:", value=f"{примечание}", inline=True)

                ChannelObject = disnake.utils.get(inter.guild.channels, id=channel)
                await ChannelObject.send(f"<@&{highstaff}> рассмотрите заявление от {inter.author.mention}", embed=emb, components=[
                disnake.ui.Button(label="Одобрить", style=disnake.ButtonStyle.success, custom_id="Approve"),
                disnake.ui.Button(label="Отклонить", style=disnake.ButtonStyle.danger, custom_id="Reject")
            ],)
                await inter.send("**🟢 Вы успешно отправили запрос!**", ephemeral=True)
            else:
                error_emb = disnake.Embed(
                    title="Ошибка",
                    description=f"Данную команду может использовать только старший и руководящий состав",
                    color = 0xDA373C,
                    timestamp=datetime.datetime.now()
                )
                await inter.response.send_message(embed=error_emb, ephemeral=True)




def setup(bot: commands.Bot):
    bot.add_cog(RequestPromotion(bot))