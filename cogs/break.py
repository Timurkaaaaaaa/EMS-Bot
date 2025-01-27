import disnake
from disnake.ext import commands
import datetime
import json
import os

config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

with open(config_path) as config:
    config = json.load(config)

channel = config['channels']['Break']
highstaff = config['roles']['HighStaff']


class Break(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def перерыв(self, inter, время_начала: str, время_окончания: str):
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
                   title="Перерыв",
                   color = 0x2B2D31,
                   timestamp=datetime.datetime.now()
               )
               emb.add_field(name="Время начала: ", value=f"{время_начала}", inline=False)
               emb.add_field(name="Время окончания: ", value=f"{время_окончания}", inline=True)

               department=-1

                              # Найти отдел пользователя
               departments = config['roles']['departments']
               department = None

               for role in inter.author.roles:
                   if role.id in departments.values():
                       # Получаем ключ (название отдела) по значению (id роли)
                       department = next(
                           (key for key, value in departments.items() if value == role.id),
                           None
                       )
                       break

               # Если отдел не найден, назначаем HighStaff
               if department is None:
                   bosses = [highstaff]
               else:
                   bosses = config['roles']['bosses'][department]

               # Формируем текст с упоминаниями
               bossesText = " ".join(f"<@&{boss_id}>" for boss_id in bosses)

               # Отправляем сообщение
               ChannelObject = disnake.utils.get(inter.guild.channels, id=channel)
               await ChannelObject.send(
                   f"{bossesText} рассмотрите заявление от {inter.author.mention}",
                   embed=emb,
                   components=[
                       disnake.ui.Button(label="Одобрить", style=disnake.ButtonStyle.success, custom_id="BreaksApprove"),
                       disnake.ui.Button(label="Отклонить", style=disnake.ButtonStyle.danger, custom_id="BreaksReject"),
                   ],
               )
               await inter.send("**🟢 Вы успешно отправили запрос!**", ephemeral=True)




def setup(bot: commands.Bot):
    bot.add_cog(Break(bot))