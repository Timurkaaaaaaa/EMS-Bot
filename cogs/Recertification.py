import disnake
from disnake.ext import commands

import datetime
import json
import os

config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

with open(config_path) as config:
    config = json.load(config)

channel = config['channels']['Recertification']
highstaff = config['roles']['HighStaff']



class Recertification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def переаттестация(self, inter):
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
            embed = disnake.Embed(
                title="Запрос на переаттестацию",
                color = 0x2B2D31,
                timestamp=datetime.datetime.now()
            )
            embed.add_field(name="Запросил переаттестацию:", value=f"{inter.author.mention}")
            channelObj = disnake.utils.get(inter.guild.channels, id=channel)
            await channelObj.send(f"<@&{highstaff}> рассмотрите заявление от {inter.author.mention}",embed=embed, components=[
                    disnake.ui.Button(label="Одобрить", style=disnake.ButtonStyle.success, custom_id="Approve"),
                    disnake.ui.Button(label="Отклонить", style=disnake.ButtonStyle.danger, custom_id="Reject")
                ],)
            await inter.send("**🟢 Вы успешно отправили запрос!**", ephemeral=True)




def setup(bot: commands.Bot):
    bot.add_cog(Recertification(bot))