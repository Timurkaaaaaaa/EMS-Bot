import disnake
from disnake.ext import commands
import datetime
import json
import os

bot = commands.Bot()

with open("config.json") as config:
    config = json.load(config)
bot.load_extensions("cogs")



@bot.event
async def on_ready():
    print("Бот \"Няшка бота\" готов к работе!")

highstaff = config['roles']['HighStaff']
HeadPhysician = config['roles']['HeadPhysician']
DeputyHeadPhysician = config['roles']['DeputyHeadPhysician']






bot.run("TOKEN")
