# Big Ups to: https://realpython.com/how-to-make-a-discord-bot-python/

import discord  # Make sure you've used "pip install -U discord.py"
# https://tinydb.readthedocs.io/en/stable/usage.html
from tinydb import TinyDB, Query  # "pip install -U tinydb"
import re  # regex for later, native to python
# from datetime import datetime, date # native to python
import time  # native to python

# ---
# Use .env file for configuration settings; to protect sensitive information
import os  # Load os module to access other files (.env)
from dotenv import load_dotenv  # all we need to import here is the load command "pip install -U python-dotenv"
load_dotenv()  # Get variables from .env file
PREFIX = os.getenv('DISCORD_PREFIX')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

TIMESCALE = os.getenv('TIMESCALE')

# ---
# Link DB(s)
castleDB = TinyDB('./zombieCastleDB.json')

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
    if len(castleDB) == 0:
        print('db init')
        castleDB.insert({
            "type":"systemInfo",
            # "lastCommand":"null"
        })


@client.event
async def on_message(message): # This is executed everytime a message is posted on the discord server

    if message.author.bot:  # ignore bot messages
        return

    command = ''
    messageAuthorInDB = castleDB.search(Query().playerID == message.author.id)

    if len(castleDB) > 1:
        castleInfo = castleDB.search(Query().type == "castleInfo")
        # messageAuthorInDB = castleDB.search(Query().playerID == message.author.id)


    if message.content.startswith(PREFIX) == False:
        return # Ignore non prefixed message
    else:
        # Remove all extra / duplicate spaces
        slicedMessage = re.sub(' +', ' ', message.content[(len(PREFIX)):]) # Then chop off the first few characters of the message string

        if slicedMessage.find(' ') == 0: # if there is a space left before the command (there won't be a space at the end after the above)
            command =  slicedMessage[1:] # then the string = the 1st ([0,1]) char until the end to get rid of space
        else:
            command = slicedMessage # Otherwise the whole string is the command





            # ----------
            # Start actual commands

        if command == 'version' or command == '-v':
            await message.channel.send('0.1.1')

        if command == "ls":
            response = castleDB.all()
            await message.channel.send(response)

        if command == "len":
            response = len(castleDB)
            await message.channel.send(response)

        if command == "author" or command == "me":
            if messageAuthorInDB:
                await message.channel.send(messageAuthorInDB)
            # response = messageAuthorInDB
            else:
                await message.channel.send("didn't find you in db")

        if command == "help":
            response = 'we all need help'
            await message.channel.send(response)
            



        if command == "newStronghold" or command == "new":
            if castleDB.contains(Query().type == 'castleInfo'):
                await message.channel.send('there is a castle in progress, use delStronghold')
            else:
                castleDB.insert({
                    "type": "castleInfo",
                    "health": 20,
                    "foodStored": 20,
                    "materialStored": 20
                })
                await message.channel.send('new stronghold founded')

        if command == "deleteStronghold" or command == "del":
            castleDB.truncate()
            await message.channel.send('stronghold deleted')


        if command == "castleStatus" or command == "status":
            status = castleDB.search(Query().type == "castleInfo")
            await message.channel.send(status)


        if command == "joinStronghold" or command == "join":
            if messageAuthorInDB:
                await message.channel.send('you\'re already a part of this fortress')
            else:
                castleDB.insert({
                    "type":"playerInfo",
                    "playerID": message.author.id,
                    "playerName": message.author.name,
                    "busyDoing": "idle",
                    "busyUntil":"idle",
                    "foodGathered":0,
                    "materialsGathered":0
                })
                await message.channel.send('welcome to our fortress')

    
        if command == "gatherFood" or command == "food":
            if messageAuthorInDB:
                castleDB.update({'foodGathered': 10}, Query().playerID == message.author.id)
                castleDB.update({'busyDoing': "gathering food"}, Query().playerID == message.author.id)
                # castleDB.update({'busyUntil': str(datetime.now())}, Query().playerID == message.author.id)
                castleDB.update({'busyUntil': str( int(time.time() + TIMESCALE) )}, Query().playerID == message.author.id)
                await message.channel.send('you have gone to collect food')
            else:
                await message.channel.send('you haven\'t joined this fortress yet')


        if command == 'return':
            # if castleDB.contains(Query().playerID == message.author.id):
            if messageAuthorInDB:
                foodGathered = messageAuthorInDB[0]["foodGathered"]
                foodStored = castleInfo[0]["foodStored"]
                castleDB.update({"foodStored" : foodStored + foodGathered}, Query().type == "castleInfo")
                castleDB.update({'foodGathered': 0}, Query().playerID == message.author.id)
                castleDB.update({'busyDoing': "idle"}, Query().playerID == message.author.id)
                castleDB.update({'busyUntil': "idle"}, Query().playerID == message.author.id)
                await message.channel.send('you have returned with ' + str(foodGathered) + ' food')
            else:
                await message.channel.send('you haven\'t joined this fortress yet')













client.run(TOKEN)
