import disnake
from disnake.ext import commands
from disnake import TextInputStyle
import datetime
import json
import os


config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

with open(config_path) as config:
    config = json.load(config)

channel = config['channels']['BriefingReport']
highstaff = config['roles']['HighStaff']

class BriefingReport(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def отчёт_брифинг(self, inter, проводил_брифинг: disnake.Member, проделанная_работа: str):
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
                title="Брифинг",
                color = 0x2B2D31,
                timestamp=datetime.datetime.now()
            )
            emb.add_field(name="Оставил отчёт:", value=f"{inter.author.mention}", inline=False)
            emb.add_field(name="Проводил брифинг:", value=f"<@{проводил_брифинг.id}>", inline=False)
            emb.add_field(name="Проделанная работа:", value=f"{проделанная_работа}", inline=False)

            await inter.response.send_message(f"<@{проводил_брифинг.id}> рассмотрите отчёт от {inter.author.mention}", embed = emb)




def setup(bot: commands.Bot):
    bot.add_cog(BriefingReport(bot))