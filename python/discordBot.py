# Big Ups to:
# https://realpython.com/how-to-make-a-discord-bot-python/
import re # regex for later

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
# Link DB

from tinydb import TinyDB, Query

db = TinyDB('discordDB.json')

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



@client.event
async def on_message(message):
    if message.author.bot: # ignore bot messages
        return


    command = ''
    args = ''

    if message.content.startswith(PREFIX) == False: 
        # Ignore non prefixed message
        return
    else:
        # Format message, seperate command and args
            # Remove extra spaces
        slicedMessage = re.sub(' +', ' ', message.content[(len(PREFIX)):]) 
        
        
        if slicedMessage.find(' ') == 0:
                # Remove a space at the begining
            slicedMessage = slicedMessage[1:]

        
        endOfCommand = slicedMessage.find(' ')
        if slicedMessage.find(' ') == 0:
            command = slicedMessage[0:]
        elif slicedMessage.find(' ') == -1:
            command = slicedMessage[0:]
            args = False
        else:
            command = slicedMessage[0:endOfCommand]
            args = slicedMessage[endOfCommand:]

    await message.channel.send(command)
    await message.channel.send(args)






    if command == 'test':
        response = '99'
        await message.channel.send(response)
    

    # ---
    # My special commands :P
    if message.author.id != 663600377677086730: # the number is my discord id
        return
    else:
        # Actual cmds:

        if command == 'testMe':
            response = '99!?'
            await message.channel.send(response)


        if message.content == "write db":
            print('writing to db')
            db.insert({"type":"test", "data": "a string"})
            print('db write complete')


        if message.content == 'list db':
           await message.channel.send(db.all())

















client.run(TOKEN)

