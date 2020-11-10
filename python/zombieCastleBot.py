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
DAYLENGTH = int(os.getenv('DAYLENGTH'))
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
            "highscore":0
            # "lastCommand":"null"
        })


@client.event
async def on_message(message): # This is executed everytime a message is posted on the discord server

    if message.author.bot:  # ignore bot messages
        return

    command = ''
    castleInfo = ''
    messageAuthorInDB = castleDB.search(Query().playerID == message.author.id)
    if messageAuthorInDB:
        messageAuthorInDB = messageAuthorInDB[0]

    if len(castleDB) > 1:
        castleInfo = castleDB.search(Query().type == "castleInfo")[0]
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

        timeOfMessage = int(time.time())
        dayOfMessage = int(timeOfMessage / DAYLENGTH)

        if command == 'version' or command == '-v':
            await message.channel.send('0.2.2')
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
            await message.channel.send(timeOfMessage)
            return

        if command == "today":
            await message.channel.send("today is the: " + str(dayOfMessage) + " days since the epoch")
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
                    "timeStarted":int(timeOfMessage),
                    "firstDay": int(dayOfMessage),
                    "lastDayUpdated": int(dayOfMessage),
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


        daysSinceUpdate = dayOfMessage - castleInfo["lastDayUpdated"] # difference between the message and the last day the bot did an overnight attack
        daysSurvived = dayOfMessage - castleInfo["firstDay"]

        # --- DAILY EVENTS ---
        if daysSinceUpdate: # have events been fired since the last day?
            attackDamage = daysSinceUpdate * 3
            newBarricadeTotal = castleInfo["barricade"] - attackDamage
            if newBarricadeTotal < 0: # if barricade is below 0 spill damage into health
                newHealthTotal = castleInfo["health"] + newBarricadeTotal # which will be negative to reach this point
                if newHealthTotal <= 0:
                    pointsTotal = daysSurvived * 12 + (castleInfo["foodStored"] + castleInfo["materialStored"])
                    await message.channel.send('The fortress has been overrun :( You made it to ' + str(pointsTotal) + " points!")
                    await message.channel.send("Time to start a new one!")
                    return
                castleDB.update({"health":newHealthTotal}, Query().type == "castleInfo")
            castleDB.update({"barricade": newBarricadeTotal, "lastDayUpdated": dayOfMessage}, Query().type == "castleInfo")
            
            await message.channel.send("No one has attended to the stronghold in " + str(daysSinceUpdate) + ' days, and it was attacked for ' + str(attackDamage) + " damage in all")


        if command == "deleteStronghold" or command == "del":
            castleDB.truncate()
            castleDB.insert({
                "type": "systemInfo",
                "highscore": 0
            })
            await message.channel.send('stronghold deleted')
            return

        if command == "dayDif":
            await message.channel.send(daysSinceUpdate)
            return
        if command == "days":
            await message.channel.send(daysSurvived)
            return


# ------------check stronghold isn't dead--------------
        if castleInfo["health"] < 1:
            pointsTotal = daysSurvived * 12 + (castleInfo["foodStored"] + castleInfo["materialStored"])
            await message.channel.send('The fortress has been overrun :( You made it to ' + str(pointsTotal) + " points!")
            await message.channel.send("Time to start a new one!")
            return
# -----------------------------------------------------


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
                    "joinedOn": int(time.time()),
                    "busyDoing": "idle",
                    "busyUntil":"idle",
                    "foodGathered":0,
                    "materialsGathered":0
                })
                castleDB.update({"players": castleInfo["players"] + 1 },Query().type == "castleInfo")
                await message.channel.send('welcome to our fortress')
            return



# ---------------check if user has joined--------------
        if not messageAuthorInDB:
            await message.channel.send('you haven\'t joined this fortress yet')
            return
# -----------------------------------------------------


        if command == 'return' or command == "home" or command == "done":
            authorDoing = messageAuthorInDB["busyDoing"]
            if authorDoing == "idle":
                await message.channel.send("you're not doing anything")
                return
            if messageAuthorInDB["busyUntil"] < timeOfMessage:
                if authorDoing == "gatherFood":
                    newFoodTotal = castleInfo["foodStored"] + messageAuthorInDB["foodGathered"]
                    castleDB.update({"foodStored": newFoodTotal}, Query().type == "castleInfo")
                    castleDB.update({'foodGathered': 0, 'busyDoing': "idle", 'busyUntil': "idle"}, Query().playerID == message.author.id)
                    await message.channel.send('you have returned with ' + str(messageAuthorInDB["foodGathered"]) + ' food')
                elif authorDoing == "gatherMaterial":
                    newMaterialTotal = messageAuthorInDB["materialGathered"] + castleInfo["materialStored"]
                    castleDB.update({"materialStored": newMaterialTotal}, Query().type == "castleInfo")
                    castleDB.update({'materialGathered': 0, 'busyDoing': "idle", 'busyUntil': "idle"}, Query().playerID == message.author.id)
                    await message.channel.send('you have returned with ' + str(messageAuthorInDB["materialGathered"]) + ' material')
                elif authorDoing == "barricade":
                    barricadeAdded = 10
                    castleDB.update({"barricade": castleInfo["barricade"] + barricadeAdded}, Query().type == "castleInfo")
                    castleDB.update({'busyDoing': "idle", 'busyUntil': "idle"}, Query().playerID == message.author.id)
                    await message.channel.send('You added: ' + str(barricadeAdded) + ' to the barricade')
            else:
                await message.channel.send("you're still busy")
            return


# ---------------check if user is busy-----------------
        if not messageAuthorInDB["busyDoing"] == "idle":
            await message.channel.send("You're still busy doing: " + messageAuthorInDB["busyDoing"])
            return
# -----------------------------------------------------


        if command == "gatherFood" or command == "food":
            castleDB.update({'foodGathered': 10, 'busyDoing': "gatherFood", 'busyUntil': timeOfMessage + TIMESCALE}, Query().playerID == message.author.id)
            await message.channel.send('you have gone to collect food')
            return

        if command == "gatherMaterial" or command == "material":
            castleDB.update({'materialGathered': 10, 'busyDoing': "gatherMaterial", 'busyUntil': timeOfMessage + TIMESCALE}, Query().playerID == message.author.id)
            await message.channel.send('you have gone to collect material')
            return

        if command == "barricade" or command == "repair":
            if castleInfo["materialStored"] < 20:
                await message.channel.send("you don't have enough material")
                return
            else:
                castleDB.update({"busyDoing":"barricade", "busyUntil": timeOfMessage + TIMESCALE} ,Query().playerID == message.author.id)
                castleDB.update({"materialStored": castleInfo["materialStored"] - 20}, Query().type == "castleInfo")
                await message.channel.send("you start repairing")
                return














client.run(TOKEN)
