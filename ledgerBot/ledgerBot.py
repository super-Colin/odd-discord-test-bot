# This example requires the 'members' privileged intents


from datetime import datetime, date
from google.oauth2 import service_account
import pygsheets
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

# For Gsheets
SPREADSHEET_ID = os.getenv('GSHEETS_SPREADSHEET_ID')
RANGE_NAME = os.getenv('GSHEETS_RANGE_NAME')
GSHEETS_SPREADSHEET_URL_KEY = os.getenv('GSHEETS_SPREADSHEET_URL_KEY')
    # ---
serviceAccountFile = './gCredentials.env.json'

import discord
from discord.ext import commands
import random

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
# intents.members = True

# bot = commands.Bot(command_prefix=PREFIX, description=description, intents=intents)
bot = commands.Bot(command_prefix=PREFIX, description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)



# @bot.command()
# async def pay(ctx, toMember: discord.Member, amount):
#     fromMember = ctx.author
#     """Send tokens to someone"""
#     await ctx.send(f'working on it... sending {amount} tokens to {toMember} from {fromMember}')




@bot.command()
async def headers(ctx):
    wks = await getWorkSheet()
    table = []
    for row in wks:
        table.append(row)
    # get the headers and remove them from the table
    tableHeaders = table[0]
    table.pop(0)
    # put indexes on the labels we want
    ledgerIndexes = getLabelIndexes(tableHeaders)
    msg = (f'{ledgerIndexes}')
    await ctx.send(msg)


@bot.command()
async def balance(ctx):
# async def balance(ctx, targetAccount: discord.Member):
    msg = ''
    targetAccountId = str(ctx.author.id)
    # targetAccountId = targetAccount.id
    balance = ''
    wks = await getWorkSheet()

    # create a list containing all rows from the sheet
    table=[]
    for row in wks:
        table.append(row)
    # get the headers and remove them from the table
    tableHeaders = table[0]
    table.pop(0)
    # put indexes on the labels we want
    ledgerIndexes = getLabelIndexes(tableHeaders)

    
    #loop through table
    foundIt = 'No'
    action = ''
    date = ''
    fromAccount = ''
    for row in table:
        #check if it was to our target account
        if row[ledgerIndexes['To Account ID']] == targetAccountId :
            foundIt = 'YES!!'
            balance = row[ledgerIndexes['To Account Balance']]
            action = row[ledgerIndexes['Action']]
            date = row[ledgerIndexes['Date']]
            fromAccount = row[ledgerIndexes['From Account']]

    msg = (f'Found account: {foundIt} \n The balance of {targetAccountId} is {balance} \n from a {action} on {date} from {fromAccount}')
    # msg = (f'{theRows}')
    await ctx.send(msg)


@bot.command()
async def longBalance(ctx):
    wks = await getWorkSheet()

    table = []
    for row in wks:
        table.append(row)
    tableHeaders = table[0]
    table.pop(0)

    ledgerIndexes = getLabelIndexes(tableHeaders)
    msg = (f'{ledgerIndexes}')
    # for row in table:
    #     if row[ledgerIndexes['From Account ID']] == ctx.author.id :
    #         msg =+ row[ledgerIndexes['From Account ID']]
    await ctx.send(msg)


@bot.command()
async def sheetDump(ctx):
    wks = await getWorkSheet()
    table = []
    for row in wks:
        table.append(row)
    msg = (f'{table}')
    await ctx.send(msg)


async def getWorkSheet():
    client = pygsheets.authorize(service_file=serviceAccountFile)
    sheet = client.open_by_key(GSHEETS_SPREADSHEET_URL_KEY)
    wks = sheet.worksheet_by_title('Sheet1')
    return wks

def getLabelIndexes(tableHeaders):
    # figure out what columns are the ones we want
    ledgerIndexes = {
        'Date': '',
        'Time': '',
        'Action': '',
        'From Account': 0,
        'From Account ID': 0,
        'From Account Balance': 0,
        'To Account': 0,
        'To Account ID': 0,
        'To Account Balance': 0,
        'Amount': 0,
    }
    for columnIndex, columnHeader in enumerate(tableHeaders):
        for labelString in ledgerIndexes:
            if columnHeader == labelString:
                ledgerIndexes[labelString] = columnIndex
    return ledgerIndexes















@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined in {member.joined_at}')

@bot.group()
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send(f'No, {ctx.subcommand_passed} is not cool')

@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')

bot.run(TOKEN)
