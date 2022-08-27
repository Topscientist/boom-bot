import os
import logging
import discord
from discord import app_commands

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

MY_GUILD = discord.Object(id=786182586501562378)

intents = discord.Intents.default()
bot = discord.bot(intents=intents)


bot.run(os.getenv('TOKEN'), log_handler=handler, log_level=logging.DEBUG)