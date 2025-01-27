import disnake
from disnake.ext import commands
import datetime
import json
import os


config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

with open(config_path) as config:
    config = json.load(config)

channel = config['channels']['PunishmentRequest']
highstaff = config['roles']['HighStaff']

class PunishmentRequest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def запрос_выдачи_взыскания(self, inter, нарушитель: disnake.User, ссылка_на_выговор: str):
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
                    title="Запрос на выдачу взыскания",
                    color = 0x2B2D31,
                    timestamp=datetime.datetime.now()
                )
                emb.add_field(name="Нарушитель:", value=f"{нарушитель.mention}", inline=False)
                emb.add_field(name="Выговор:", value=f"{ссылка_на_выговор}", inline=False)
                await inter.response.send_message(f"<@&{highstaff}>", embed=emb)
            else:
                error_emb = disnake.Embed(
                    title="Ошибка",
                    description=f"Данную команду может использовать только старший и руководящий состав",
                    color = 0xDA373C,
                    timestamp=datetime.datetime.now()
                )
                await inter.response.send_message(embed=error_emb, ephemeral=True)




def setup(bot: commands.Bot):
    bot.add_cog(PunishmentRequest(bot))