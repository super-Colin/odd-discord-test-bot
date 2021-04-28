# # Big Ups to: https://realpython.com/how-to-make-a-discord-bot-python/

# import discord  # Make sure you've used "pip install -U discord.py"
# from tinydb import TinyDB, Query  # "pip install -U tinydb"
# import re  # regex for later, native to python
# import random
# from datetime import datetime, date # native to python

# # ---
# # Use .env file for configuration settings; to protect sensitive information
# import os  # Load os module to access other files (.env)
# from dotenv import load_dotenv  # all we need to import here is the load command "pip install -U python-dotenv"
# load_dotenv()  # Get variables from .env file
# PREFIX = os.getenv('DISCORD_PREFIX')
# TOKEN = os.getenv('DISCORD_TOKEN')
# GUILD = os.getenv('DISCORD_GUILD')
# # GUILD_MAIN_CHANNEL_ID = os.getenv('GUILD_MAIN_CHANNEL_ID')

# # ---
# # Link DB(s)
# mentionDB = TinyDB('./zombiementionDB.json')

# # ---
# # Set up bot

# # Initialize bot and store it in a variable for easy access
# client = discord.Client()







def isOdd(number):
    if number % 2 == 0:
        # print('Number is ODD: ' + str(number))
        return False
    else:
        return True

def isEven(number):
    if number % 2 == 0:
        # print('Number is EVEN: ' + str(number))
        return True
    else:
        return False

numberLength = 4

def evenOdd(number):
    numberAsString = str(number)
    onNumber = 0
    for num in numberAsString:
        # print('starting number: ' + num)
        num = int(num)
        onNumber = onNumber + 1
        if isEven(num):
            print('number is even: ' + str(num) )
        else:
            print('number is odd: ' + str(num))


evenOdd(1224)

