
# ---
# Use .env file for configuration settings

import os
    # Load os module to access other files (.env)
from dotenv import load_dotenv
    # Import load_dotenv command from python-dotenv module
        # Use the CLI cmd "pip install -U python-dotenv" to make sure you have dotenv installed

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')



# ---
# Set up bot

import discord
    # Import discord bot library

client = discord.Client()
    # Initialize bot and store it in a variable for easy access



@client.event
async def on_ready():
    print(f'{client.user} has connected!')


client.run(TOKEN)

