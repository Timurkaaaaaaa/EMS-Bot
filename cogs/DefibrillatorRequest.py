import disnake
from disnake.ext import commands
import datetime
import json
import os

config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

with open(config_path) as config:
    config = json.load(config)

channel = config['channels']['DefibrillatorRequest']
highstaff = config['roles']['HighStaff']


class DefibrillatorRequest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def запрос_дефибрилятора(self, inter, ранг: int):
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
                title="Запрос дефибрилятора",
                color = 0x2B2D31,
                timestamp=datetime.datetime.now()
            )
            emb.add_field(name="Запрашивает: ", value=f"{inter.author.mention}")
            emb.add_field(name="Ранг: ", value=f"{str(ранг)}")
            ChannelObject = disnake.utils.get(inter.guild.channels, id=channel)
            await ChannelObject.send(f"<@&{highstaff}> рассмотрите заявление от {inter.author.mention}", embed=emb, components=[
            disnake.ui.Button(label="Одобрить", style=disnake.ButtonStyle.success, custom_id="DefibrillatorApprove"),
            disnake.ui.Button(label="Отклонить", style=disnake.ButtonStyle.danger, custom_id="DefibrillatorReject")
        ],)
            await inter.send("**🟢 Вы успешно отправили запрос!**", ephemeral=True)




def setup(bot: commands.Bot):
    bot.add_cog(DefibrillatorRequest(bot))