
import re # regex for later
from datetime import datetime, date
# ---
# Use .env file for configuration settings

import os
    # Load os module to access other files (.env)
from dotenv import load_dotenv
    # Import load_dotenv command from python-dotenv module
    # Use the CLI cmd "pip install -U python-dotenv" to make sure you have dotenv installed
load_dotenv() # Get variables from .env file
PREFIX = os.getenv('DISCORD_PREFIX')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_MAIN_CHANNEL_ID = os.getenv('GUILD_MAIN_CHANNEL_ID')

    # ---


import discord

from discord.ext import commands




bot = commands.Bot(command_prefix='.', description="Test bot")







client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author.bot:
        return 

    if message.content.startswith('?/coinTo'):
        await message.channel.send('send coin to...')



client.run(TOKEN)


