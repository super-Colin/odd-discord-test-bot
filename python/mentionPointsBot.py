# Big Ups to: https://realpython.com/how-to-make-a-discord-bot-python/

import discord  # Make sure you've used "pip install -U discord.py"
from tinydb import TinyDB, Query  # "pip install -U tinydb"
import re  # regex for later, native to python
import random
from datetime import datetime, date # native to python

# ---
# Use .env file for configuration settings; to protect sensitive information
import os  # Load os module to access other files (.env)
from dotenv import load_dotenv  # all we need to import here is the load command "pip install -U python-dotenv"
load_dotenv()  # Get variables from .env file
PREFIX = os.getenv('DISCORD_PREFIX')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
# GUILD_MAIN_CHANNEL_ID = os.getenv('GUILD_MAIN_CHANNEL_ID')

# ---
# Link DB(s)
mentionDB = TinyDB('./zombiementionDB.json')

# ---
# Set up bot

# Initialize bot and store it in a variable for easy access
client = discord.Client()



# Support for multiple server connections
@client.event
async def on_ready():  # This is executed when you first run the script to get the bot running
    guild = discord.utils.get(client.guilds, name=GUILD)

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name} (id: {guild.id})\n'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

    # Check for or init DB
    if len(mentionDB) == 0:
        print('db init')
        # today = datetime.today().date()
        mentionDB.insert({
            "type":"systemInfo",
            # "lastCommand":"null"
        })


@client.event
async def on_message(message): # This is executed everytime a message is posted on the discord server

    if message.author.bot:  # ignore bot messages
        return

    # systemInfoEntry = mentionDB.search(Query().type == "systemInfo")
    command = ''
    messageAuthorInDB = mentionDB.search(Query().playerID == message.author.id)

    if message.content.startswith(PREFIX) == False:
        return # Ignore non prefixed message
    else:
        # Remove all extra / duplicate spaces
        slicedMessage = re.sub(' +', ' ', message.content[(len(PREFIX)):]) # Then chop off the first few characters of the message string

        if slicedMessage.find(' ') == 0: # if there is a space left before the command (there won't be a space at the end after the above)
            command =  slicedMessage[1:] # then the string = the 1st ([0,1]) char until the end to get rid of space
        else:
            command = slicedMessage # Otherwise the whole string is the command


        if command == "ls":
            response = mentionDB.all()
            await message.channel.send(response)

        if command == "auth":
            response = messageAuthorInDB
            await message.channel.send(response)

        if command == "help":
            response = 'we all need help'
            await message.channel.send(response)
        
        if message.mentions:
            if len(message.mentions) == 1:
                await message.channel.send('points to ' + str(message.mentions[0].nick))
            else:                
                await message.channel.send('points to ' + str(message.mentions))

        if command == "roll6":
            response = random.randint(1, 6)
            if message.author.id == 663600377677086730:
                response = '7 soo much crit'
            await message.channel.send(response)

        if command == "roll20":
            response = random.randint(1, 20)
            if message.author.id == 663600377677086730:
                response = '21 soo much crit'
            await message.channel.send(response)

        if command == "roll100":
            response = random.randint(1, 100)
            if message.author.id == 663600377677086730:
                response = '101 soo much crit'
            await message.channel.send(response)


client.run(TOKEN)
