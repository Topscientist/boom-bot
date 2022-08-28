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

MY_GUILD = discord.Object(id=832676807970783332)

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
        self.tree.copy_global_to(guild=discord.Object(id=786182586501562378))
        await self.tree.sync(guild=discord.Object(id=786182586501562378))

intents = discord.Intents.default()
client = MyClient(intents=intents)

@client.event
async def on_ready():
    print ('The bot is about to go boom!')
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print ('-----------')
    await client.change_presence(activity=discord.Game(name="with the code from https://github.com/Topscientist/discord-slash-commands"))

@client.tree.command()
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message(f':wave: Hi, {interaction.user.mention}!')

@client.tree.command()
async def whatisthis(interaction: discord.Interaction):
    """What on earth is this?"""
    await interaction.respond.send_message(f"So {interaction.user.mention}, you're curious about this project? Well, this is a test to see what happens when the open-source community is allowed to run rampant with bot code :>. You can edit my code over here: https://github.com/Topscientist/boom-bot")

@client.tree.command()
@app_commands.describe(member='The member you want to get the joined date from; defaults to the user who uses the command')
async def joined(interaction: discord.Interaction, member: Optional[discord.Member] = None):
    """Get the date when a user joined."""
    # If no member is explicitly provided then we use the command user here
    member = member or interaction.user

    # The format_dt function formats the date time into a human readable representation in the official client
    await interaction.response.send_message(f'{member} joined {discord.utils.format_dt(member.joined_at)}')

client.run(os.getenv('TOKEN'), log_handler=handler, log_level=logging.DEBUG)
