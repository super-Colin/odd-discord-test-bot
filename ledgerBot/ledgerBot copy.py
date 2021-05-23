
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
    # ---


import discord

from discord.ext import commands




bot = commands.Bot(command_prefix=PREFIX, description="Test bot")




@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(pass_context=True)
async def chooser(ctx):
    """Simple choosing option from bot"""

    # Hard coded items
    choices = ['A', 'B', 'C']
    message = ''

    # Format for showing the choices
    choiceLen = len(choices)
    for no, choice in zip(range(choiceLen), choices):
        message += str(no + 1) + ' ' + choice + '\n'

    await bot.say(message)

    # Function for checking if the next message is digit and between 1 and 3
    def guess_check(m):
        return m.content.isdigit() and int(m.content) >= 1 and int(m.content) <= len(choices)

    # Wait for user message who send this command for timeout (seconds) and pass the function check
    guess = await bot.wait_for_message(timeout=5.0, author=ctx.message.author, check=guess_check)


    if guess is None: 
        # If Timeout 
        await bot.say('None')
    else:
        # If not timeout and pass the check
        # Convert message content to int
        guess = int(guess.content)
        # Send the choice
        await bot.say(choices[guess - 1])


bot.run(TOKEN)