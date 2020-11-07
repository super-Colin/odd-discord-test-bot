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

TIMESCALE = int(os.getenv('TIMESCALE'))
DIFFICULTYSCALE = float(os.getenv('DIFFICULTYSCALE'))

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
    castleInfo = ''
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




            # ------------------------------
            # ---------------------------------------------------
            # Start actual commands

        if command == 'version' or command == '-v':
            await message.channel.send('0.1.4')
            return

        if command == "ls" or command == "db":
            response = castleDB.all()
            await message.channel.send(response)
            return

        if command == "len":
            response = len(castleDB)
            await message.channel.send(response)
            return

        if command == "author" or command == "me":
            if messageAuthorInDB:
                await message.channel.send(messageAuthorInDB)
            else:
                await message.channel.send("didn't find you in db")
            return

        if command == "now":
            await message.channel.send(int(time.time()))
            return

        if command == "help":
            response = 'we all need help'
            await message.channel.send(response)
            return




        if command == "newStronghold" or command == "new":
            if castleDB.contains(Query().type == 'castleInfo'):
                await message.channel.send('there is a castle in progress, use delStronghold')
            else:
                castleDB.insert({
                    "type": "castleInfo",
                    "players": 0,
                    "serfs": 0,
                    "health": 20,
                    "barricade": 20,
                    "foodStored": 20,
                    "materialStored": 20
                })
                await message.channel.send('new stronghold founded')
            return


# ------------check if there is a stronghold-----------
        if not castleInfo:
            await message.channel.send('there is no fortress')
            return
# -----------------------------------------------------


        if command == "deleteStronghold" or command == "del":
            castleDB.truncate()
            castleDB.insert({
                "type": "systemInfo",
                # "lastCommand":"null" # This might be useful in another system, but as a discord bot it already has a full command (and response) history
            })
            await message.channel.send('stronghold deleted')
            return


        if command == "castleStatus" or command == "status" or command == "base":
            status = castleDB.search(Query().type == "castleInfo")
            await message.channel.send(status)
            return


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
                castleDB.update({"players": castleInfo[0]["players"] + 1 },Query().type == "castleInfo")
                await message.channel.send('welcome to our fortress')
            return


# ---------------check if user has joined--------------
        if not messageAuthorInDB:
            await message.channel.send('you haven\'t joined this fortress yet')
            return
# -----------------------------------------------------


        if command == 'return' or command == "home" or command == "done":
            authorDoing = messageAuthorInDB[0]["busyDoing"]
            if authorDoing == "idle":
                await message.channel.send("you're not doing anything")
                return
            if messageAuthorInDB[0]["busyUntil"] < int(time.time()):
                if authorDoing == "gatherFood":
                    foodGathered = messageAuthorInDB[0]["foodGathered"]
                    foodStored = castleInfo[0]["foodStored"]
                    castleDB.update({"foodStored": foodStored + foodGathered}, Query().type == "castleInfo")
                    castleDB.update({'foodGathered': 0}, Query().playerID == message.author.id)
                    castleDB.update({'busyDoing': "idle"}, Query().playerID == message.author.id)
                    castleDB.update({'busyUntil': "idle"}, Query().playerID == message.author.id)
                    await message.channel.send('you have returned with ' + str(foodGathered) + ' food')
                elif authorDoing == "gatherMaterial":
                    materialGathered = messageAuthorInDB[0]["materialGathered"]
                    materialStored = castleInfo[0]["materialStored"]
                    castleDB.update({"materialStored": materialStored + materialGathered}, Query().type == "castleInfo")
                    castleDB.update({'materialGathered': 0}, Query().playerID == message.author.id)
                    castleDB.update({'busyDoing': "idle"}, Query().playerID == message.author.id)
                    castleDB.update({'busyUntil': "idle"}, Query().playerID == message.author.id)
                    await message.channel.send('you have returned with ' + str(materialGathered) + ' material')
                elif authorDoing == "barricade":
                    barricadeAdded = 10
                    castleDB.update({"barricade": castleInfo[0]["barricade"] + barricadeAdded}, Query().type == "castleInfo")
                    castleDB.update({'busyDoing': "idle"}, Query().playerID == message.author.id)
                    castleDB.update({'busyUntil': "idle"}, Query().playerID == message.author.id)
                    await message.channel.send('You added: ' + str(barricadeAdded) + ' to the barricade')
            else:
                await message.channel.send("you're still busy")
            return


# ---------------check if user is busy-----------------
        if not messageAuthorInDB[0]["busyDoing"] == "idle":
            await message.channel.send("You're still busy doing: " + messageAuthorInDB[0]["busyDoing"])
            return
# -----------------------------------------------------


        if command == "gatherFood" or command == "food":
            castleDB.update({'foodGathered': 10}, Query().playerID == message.author.id)
            castleDB.update({'busyDoing': "gatherFood"}, Query().playerID == message.author.id)
            castleDB.update({'busyUntil': int(time.time()) + TIMESCALE }, Query().playerID == message.author.id)
            await message.channel.send('you have gone to collect food')
            return
        if command == "gatherMaterial" or command == "material":
            castleDB.update({'materialGathered': 10}, Query().playerID == message.author.id)
            castleDB.update({'busyDoing': "gatherMaterial"}, Query().playerID == message.author.id)
            castleDB.update({'busyUntil': int(time.time()) + TIMESCALE }, Query().playerID == message.author.id)
            await message.channel.send('you have gone to collect material')
            return

        if command == "barricade" or command == "repair":
            if castleInfo[0]["materialStored"] < 20:
                await message.channel.send("you don't have enough material")
                return
            else:
                castleDB.update({"busyDoing":"barricade"} ,Query().playerID == message.author.id)
                castleDB.update({"busyUntil": int(time.time()) + TIMESCALE }, Query().playerID == message.author.id)
                castleDB.update({"materialStored": castleInfo[0]["materialStored"] - 20}, Query().type == "castleInfo")
                await message.channel.send("you start repairing")
                return














client.run(TOKEN)
