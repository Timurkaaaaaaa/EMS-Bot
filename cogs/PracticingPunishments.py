import disnake
from disnake.ext import commands
from disnake import TextInputStyle
import datetime
import json
import os


config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

with open(config_path) as config:
    config = json.load(config)

channel = config['channels']['PracticingPunishments']
highstaff = config['roles']['HighStaff']

class PracticingPunishments(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def отработка_взыскания(self, inter, ссылка_на_взыскание: str, доказательства_отработки: str,):
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
            emb = disnake.Embed (
                title="Отработка",
                color = 0x2B2D31,
                timestamp=datetime.datetime.now()
            )
            emb.add_field(name="Отработал:", value=f"{inter.author.mention}")
            emb.add_field(name="Доказательства:", value=f"{доказательства_отработки}")

            highstaffObj = disnake.utils.get(inter.guild.roles, id=highstaff)
            await inter.response.send_message(f"{highstaffObj.mention} рассмотрите заявление от {inter.author.mention}", embed = emb, components=[
                       disnake.ui.Button(label="Одобрить", style=disnake.ButtonStyle.success, custom_id="Approve"),
                       disnake.ui.Button(label="Отклонить", style=disnake.ButtonStyle.danger, custom_id="Reject"),
                   ],)




def setup(bot: commands.Bot):
    bot.add_cog(PracticingPunishments(bot))