# Big Ups to:
# https://realpython.com/how-to-make-a-discord-bot-python/
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
    
    # Init DB for daily checks
    if len(db) == 0:
        print('db init')
        today = datetime.today().date()
        db.insert({"type":"systemInfo", "eventsCheckedOn": str(today)})



@client.event
async def on_message(message):
    if message.author.bot: # ignore bot messages
        return
    
    systemInfoEntry = db.search(Query().type == "systemInfo")
        

    # CHECK FOR DAILY EVENTS
    if datetime.strptime(systemInfoEntry[0]['eventsCheckedOn'], "%Y-%m-%d").date() < datetime.today().date():
        print('Checking daily events')
        mainChannel = client.get_channel(int(GUILD_MAIN_CHANNEL_ID))

        todayDate = datetime.today().date()

        events = db.search(Query().type == 'reminder')
        for event in events:
            eventDate = datetime.strptime(event['date'], "%Y-%m-%d").date()

            if eventDate == todayDate:
                response =  str(event['usersToRemind']) + '\n' + str(event['eventName']) + ' : ' + str(event['reminderText'])
                await mainChannel.send(response)

        # await mainChannel.send('there was an event today')


        db.update({"eventsCheckedOn": str(todayDate)}, Query().type == "systemInfo")
        print('Daily Events checked and eventsCheckedOn updated with ' + str(todayDate))
    # else:
    #     print('Daily events already checked today')
        




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
        if slicedMessage.find(' ') == 0 and slicedMessage.find(' ', 1) != -1 :
            command = slicedMessage[0:]
            args = False
        elif slicedMessage.find(' ') == -1:
            command = slicedMessage[0:]
            args = False
        else:
            command = slicedMessage[0:endOfCommand]
            args = slicedMessage[endOfCommand + 1:]


            # If parenthesis split up csv's
        if args != False:
            print('args not false')
            print(args.find('('))
            if args.find('(') == 1 or args.find('(') == 0:
                endOfArgs = args.find(')')
                regexp = '\s?([\s?a-zA-Z\d\/\'"-]+),?'
                args = re.findall(regexp, args[1:endOfArgs])




                
    #         # --- For debugging ---
    # await message.channel.send('Command : ' + command)
    # if args:
    #     await message.channel.send('args : ')
    #     await message.channel.send(args)
    # # if args[1]:
    # #     for arg in args:
    # #         await message.channel.send(arg)
    # else:
    #     await message.channel.send('args : None')






    if command == 'test':
        response = '99'
        await message.channel.send(response)
    

    # ---
    # My special commands :P
    if message.author.id != 663600377677086730: # the number is my discord id
        return
    else:
        # Actual cmds:

        # if command == '?/sc':
        #     await message.channel.send('SuperColin is Awesome')

        if command == 'testMe':
            response = '99!?'
            await message.channel.send(response)



        if command == "db.add": # (date, string)
            db.insert({"type": 'test', "date": args[0], "event": args[1]})
            await message.channel.send('db write complete')


        if command == 'db.list':
            await message.channel.send(db.all())


        if command == 'db.clear':
            db.truncate()
            await message.channel.send('db cleared')




        if command =='reminder.create': # (date [0], eventName [1], reminderText [2], repeat [3])
                # Check inputs
            inputsValid = True

            try:
                datetime.strptime(args[0], '%Y-%m-%d')
            except ValueError:
                inputsValid = False
                await message.channel.send('date not formatted correctly')

            repeatOptions = ['none', 'weekly', 'monthly', 'yearly']
            foundRepeatOption = False
            print('args: ' + str(args))
            print('option: ' + str(args[3]) )
            for option in repeatOptions:
                if option == args[3]:
                    print('option: ' + str(option) + str(args[3]))
                    foundRepeatOption = True

            if foundRepeatOption == False:
                await message.channel.send('repeat option not found')
                inputsValid = False
            
            # HELP
            if args == 'help':
                await message.channel.send('(\ndate: day/month/year "2025-12-21",\neventName: String,\nreminderText: String,\nrepeat: "none" OR "weekly" OR "monthly" OR "yearly",\nusersToRemind: @Someone, @AnotherPerson, @MorePeople < These must be mentions\n)')
                
                await message.channel.send('Try something like:\n' + PREFIX + command + ' (2021-08-25, Bot Birthday, I\'m just a bot, none, @TestBot, @Free)')

                return

            # Actually save to db
            if inputsValid:
                userMentions = []
                allUserMentions = message.mentions
                for userMentioned in allUserMentions:
                    userMentions.append(userMentioned.mention)
                userMentionsString = ', '.join(userMentions)

                db.insert({"type": 'reminder', "date": args[0], "eventName":args[1], "reminderText": args[2], "repeat": args[3], "usersToRemind": userMentionsString } )
                await message.channel.send('db entry saved')



        if command =='listChannels':
            for guild in client.guilds:
                for channel in guild.channels:
                    print(str(channel) + " - " + str(channel.id))


        if command == 'announce':
            mainChannel = client.get_channel(int(GUILD_MAIN_CHANNEL_ID))
            print(mainChannel)
            # text.replace('@everyone', 'everyone') # \u200b is our condom
            mentionString = message.author.mention
            await mainChannel.send('anoucement!! @\u200bSuperColin')
            # print(mentionString)
            await mainChannel.send('anoucement!!' + mentionString)




        if command == 'at':
            mainChannel = client.get_channel(int(GUILD_MAIN_CHANNEL_ID))
            userMention = message.mentions[0].mention
            await mainChannel.send('at ' + userMention)




        # if command == 'createEvent':
        #     mainChannel = client.get_channel(int(GUILD_MAIN_CHANNEL_ID))

        #     userMentions = []
        #     allUserMentions = message.mentions
        #     for userMentioned in allUserMentions:
        #         userMentions.append(userMentioned.mention)

        #     userMentionsString = ', '.join(userMentions)
        #     print('mentions : ')
        #     print(userMentions)
        #     response = 'at ' + userMentionsString
        #     db.insert({"type": "event", "users": userMentionsString})
        #     await mainChannel.send(response)

        if command == 'createEvent':
            mainChannel = client.get_channel(int(GUILD_MAIN_CHANNEL_ID))


            userMentions = []
            allUserMentions = message.mentions
            for userMentioned in allUserMentions:
                userMentions.append(userMentioned.mention)
            userMentionsString = ', '.join(userMentions)

            db.insert({"type": "event", "users": userMentionsString})
            
            await mainChannel.send('Event saved')



        if command == 'listEvents':
            await message.channel.send(db.search(Query().type == "event"))







client.run(TOKEN)

