# Big Ups to:
# https://realpython.com/how-to-make-a-discord-bot-python/

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



# ---
# Set up bot

import discord
    # Import discord bot library 
        # Make sure you've used "pip install -U discord.py"

client = discord.Client()
    # Initialize bot and store it in a variable for easy access



# Simple version for only one server:
    # @client.event
    # async def on_ready():
    #     print(f'{client.user} has connected!')
    #         # Print in console that bot has connected


# More robust version with support for multiple server connections
@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name} (id: {guild.id})\n'
    )
    # members = '\n - '.join([member.name for member in guild.members])
    # print(f'Guild Members:\n - {members}')


# @client.event
# async def on_some(member):
#     await member.create_dm()
#     await member.dm_channel.send(
#         'pssst.. hey kid, you should throw SuperColin a dollar'
#     )


@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content == '99!':
        response = '99!'
        # print(message.author.id)
        await message.channel.send(response)

    # My special commands :P
    if message.author.id != 663600377677086730: # the number is my discord id
        return
        # Actual cmds:
    else:
        if message.content == '?':
            response = '99!?'
            await message.channel.send(response)
        if message.content == "write db":
            














client.run(TOKEN)

