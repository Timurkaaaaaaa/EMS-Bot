import disnake
from disnake.ext import commands
from disnake import TextInputStyle
import datetime
import json
import os


config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

with open(config_path) as config:
    config = json.load(config)

channel = config['channels']['AppealingPunishments']
highstaff = config['roles']['HighStaff']

class AppealingPunishments(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def обжаловть_взыскание(self, inter, описание_ситуации: str, ссылка_на_взыскание: str, кто_выдал: disnake.User, *, доказательства: str = ""):
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
                title="Обжалование",
                color = 0x2B2D31,
                timestamp=datetime.datetime.now()
            )
            emb.add_field(name="Запрашивает обжалование:", value=f"{inter.author.mention}", inline=False)
            emb.add_field(name="Описание ситуации:", value=f"{описание_ситуации}", inline=False)
            emb.add_field(name="Взыскание:", value=f"{ссылка_на_взыскание}", inline=False)
            emb.add_field(name="Взыскание выдал:", value=f"{кто_выдал.mention}", inline=True)
            if доказательства != "":
                emb.add_field(name="Доказательства:", value=f"{доказательства}", inline=False)

            highstaffObj = disnake.utils.get(inter.guild.roles, id=highstaff)
            await inter.response.send_message(f"{highstaffObj.mention}", embed = emb)




def setup(bot: commands.Bot):
    bot.add_cog(AppealingPunishments(bot))