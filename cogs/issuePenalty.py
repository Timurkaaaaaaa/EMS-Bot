import disnake
from disnake.ext import commands
import datetime
import json
import os

import sqlite3

connection = sqlite3.connect('Punishments.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Punishments (
id INTEGER,
reason TEXT,
perpetrator INTEGER,
hours INTEGER,
proof TEXT
)
''')

connection.commit()

config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

with open(config_path) as config:
    config = json.load(config)

channel = config['channels']['issuePenalty']
highstaff = config['roles']['HighStaff']


class Dropdown(disnake.ui.StringSelect):
    def __init__(self):
        options = [
            disnake.SelectOption(
                label="Замечание 1/3", description="Три замечания приравниваются к одному выговору.", emoji="🟡"
            ),
            disnake.SelectOption(
                label="Замечание 2/3", description="Три замечания приравниваются к одному выговору.", emoji="🟡"
            ),
            disnake.SelectOption(
                label="Выговор 1/3", description="Три выговора приравниваются к Переаттестации.", emoji="🟠"
            ),
            disnake.SelectOption(
                label="Выговор 2/3", description="Три выговора приравниваются к Переаттестации.", emoji="🟠"
            ),

            disnake.SelectOption(
                label="Переаттестация", description="Сотрудник лишается возможности оказывать какие-либо услуги", emoji="⭕"
            ),
            disnake.SelectOption(
                label="Увольнение", description="Максимальная мера пресечения нарушения/нарушений", emoji="🔴"
            ),

            disnake.SelectOption(
                label="Дежурство", description="1 час и более работы в больнице", emoji="🟢"
            ),

            disnake.SelectOption(
                label="Понижение", description="", emoji="⚪"
            ),

            disnake.SelectOption(
                label="Перевод из отделения", description="", emoji="🔵"
            ),
            disnake.SelectOption(
                label="Изъятие квалификации", description="", emoji="🔵"
            ),
        ]

        super().__init__(
            placeholder="Степень наказания",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, inter: disnake.MessageInteraction):
        emb = disnake.Embed(
                   title="Взыскание",
                   color = 0x2B2D31,
                   timestamp=datetime.datetime.now()
               )
        cursor.execute('SELECT id, reason, perpetrator, hours, proof FROM Punishments WHERE id == ?', (inter.author.id,))
        results = cursor.fetchall()[0]
        cursor.execute('DELETE FROM Punishments WHERE id = ?', (inter.author.id,))
        emb.add_field(name="Выдал взыскание: ", value=f"<@{inter.author.id}>", inline=False)
        emb.add_field(name="Получил взыскание: ", value=f"<@{results[2]}> ", inline=False)
        emb.add_field(name="Степень наказания: ", value=f"{self.values[0]}", inline=False)
        emb.add_field(name="Нарушение: ", value=f"> {results[1]}", inline=True)
        emb.add_field(name="Время на отработку: ", value=f"{results[3]} час(ов)", inline=False)
        emb.add_field(name="Доказательство: ", value=f"{results[4]}", inline=False)
        #user = disnake.utils.get(inter.guild.members, id=int(results[2]))
        #print(user)
        #print(results[2])
        #if self.values[0] == "Выговор 1/3":
        #    role = disnake.utils.get(inter.guild.roles, id=config['roles']['punishments']['rebuke 1/3'])
        #    await user.add_roles(role)
        #elif self.values[0] == "Выговор 2/3":
        #    role = disnake.utils.get(inter.guild.roles, id=config['roles']['punishments']['rebuke 2/3'])
        #    await user.add_roles(role)
        #elif self.values[0] == "Переаттестация":
        #    role = disnake.utils.get(inter.guild.roles, id=config['roles']['punishments']["recertification"])
        #    await user.add_roles(role)
        ChannelObject = disnake.utils.get(inter.guild.channels, id=channel)
        await ChannelObject.send(f"{inter.author.mention} выдал взыскание <@{results[2]}>", embed=emb)
        await inter.send("**🟢 Вы успешно выдали взыскание!\n-# Если роль взыскания существует - она была выдана**", ephemeral=True, delete_after=30)


class DropdownView(disnake.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(Dropdown())


class IssuePenalty(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def выдать_взыскание(self, inter, нарушитель: disnake.User, нарушение: str, часы_на_отработку: int, доказательство: str):
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
                cursor.execute('INSERT INTO Punishments (id, reason, perpetrator, hours, proof) VALUES (?, ?, ?, ?, ?)', (inter.author.id, нарушение, нарушитель.id, часы_на_отработку, доказательство))
                view = DropdownView()
                await inter.response.send_message("**Выберите тип взыскания**", ephemeral=True, view=view)
            else:
                error_emb = disnake.Embed(
                    title="Ошибка",
                    description=f"Данную команду может использовать только старший и руководящий состав",
                    color = 0xDA373C,
                    timestamp=datetime.datetime.now()
                )
                await inter.response.send_message(embed=error_emb, ephemeral=True)




def setup(bot: commands.Bot):
    bot.add_cog(IssuePenalty(bot))
