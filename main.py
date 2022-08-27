import os

from typing import Optional

import logging

import discord
from discord import app_commands

from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('/workspaces/discord-slash-commands/TOKEN.env')

load_dotenv(dotenv_path=dotenv_path)

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

MY_GUILD = discord.Object(id=786182586501562378)

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

intents = discord.Intents.default()
client = MyClient(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print ('-----------')
    await client.change_presence(activity=discord.Game(name="with the code from https://github.com/Topscientist/discord-slash-commands"))

@client.tree.command()
async def hello(interaction: discord.Interaction):
    """Says hello! [GitHub Repo Test]"""
    await interaction.response.send_message(f':wave: Hi, {interaction.user.mention}!')

@client.tree.command()
async def whatisthis(interaction: discord.Interaction):
    """What on earth is this? [GitHub Repo Test]"""
    await interaction.respond.send_message(f"So {interaction.user.mention}, you're curious about this project? Well, ")

client.run(os.getenv('TOKEN'), log_handler=handler, log_level=logging.DEBUG)
