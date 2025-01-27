import disnake
from disnake.ext import commands
import datetime
import json
import os

config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

with open(config_path) as config:
    config = json.load(config)

channel = config['channels']['ChangeData']
highstaff = config['roles']['HighStaff']


class ChangeData(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def смена_данных(self, inter, старые_данные: str, новые_данные: str):
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
               title="Смена данных",
               color = 0x2B2D31,
               timestamp=datetime.datetime.now()
           )
           emb.add_field(name="Сотрудник: ", value=f"<@{inter.author.id}>", inline=False)
           emb.add_field(name="Старые данные: ", value=f"{старые_данные}", inline=True)
           emb.add_field(name="Новые данные: ", value=f"{новые_данные}", inline=True)
           ChannelObject = disnake.utils.get(inter.guild.channels, id=channel)
           await ChannelObject.send(f"<@&{highstaff}> рассмотрите заявление от {inter.author.mention}", embed=emb, components=[
           disnake.ui.Button(label="Одобрить", style=disnake.ButtonStyle.success, custom_id="Approve"),
           disnake.ui.Button(label="Отклонить", style=disnake.ButtonStyle.danger, custom_id="Reject")
       ],)
           await inter.send("**🟢 Вы успешно отправили запрос!**", ephemeral=True)



def setup(bot: commands.Bot):
    bot.add_cog(ChangeData(bot))