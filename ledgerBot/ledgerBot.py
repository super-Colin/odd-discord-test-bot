# pip install python-dotenv, discord, bs4, requests...
# Getting and working with Google spreadsheet
from datetime import datetime, date
from google.oauth2 import service_account
import pygsheets

# Scraping a price for Etherium
from bs4 import BeautifulSoup
import requests

# Discord bot library and command extension
import discord
from discord.ext import commands
import random
import asyncio


# ---
# Use .env file for configuration settings
import os
from dotenv import load_dotenv
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

ledgerColumns = [
    'Date',
    'Time',
    'Action',
    'From Account',
    'From Account ID',
    'From Account Balance',
    'To Account',
    'To Account ID',
    'To Account Balance',
    'Amount',
    'Description'
]





botDescription = '''The ODD oracle, always expan.'''
intents = discord.Intents.default()
# intents.members = True
bot = commands.Bot(command_prefix=PREFIX, description=botDescription)

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



@bot.command()
async def pay(ctx, toMember: discord.Member, amount):
    fromMember = ctx.author
    """Send tokens to someone"""
    await ctx.send(f'Send {amount} tokens to {toMember}? \nUse a 👍 reaction, to confirm')

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) == '👍'

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=20.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('👎 Ahh for real')
    else:
        await ctx.send('👍 Thanks brah')



# ~~~~~~~~~~~~~ Ledger Functions ~~~~~~~~~~~~~
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
async def write(ctx, targetAccount: discord.Member = None):
    if targetAccount == None:
        targetAccountId = targetAccountId = str(ctx.author.id)
    else:
        targetAccountId = str(targetAccount.id)
    wks = await getWorkSheet()
    table = []
    for row in wks:
        table.append(row)
    tableHeaders = table[0]
    table.pop(0)
    ledgerIndexes = getLabelIndexes(tableHeaders)

@bot.command()
# async def balance(ctx):
async def balance(ctx, targetAccount: discord.Member = None):
    if targetAccount == None:
        targetAccountId = targetAccountId = str(ctx.author.id)
    else:
        targetAccountId = str(targetAccount.id)
    
    wks = await getWorkSheet()

    # create a list containing all rows from the sheet
    table=[]
    for row in wks:
        table.append(row)
    tableHeaders = table[0]
    table.pop(0)
    ledgerIndexes = getLabelIndexes(tableHeaders)
    #loop through table
    foundIt, action, date, fromAccount, toAccount, balance, description = False,'','','','','',''
    for row in table:
        #check if it was to our target account
        if row[ledgerIndexes['To Account ID']] == targetAccountId :
            foundIt = True
            balance = row[ledgerIndexes['To Account Balance']]
            action = row[ledgerIndexes['Action']]
            date = row[ledgerIndexes['Date']]
            fromAccount = row[ledgerIndexes['From Account']]
            toAccount = row[ledgerIndexes['To Account']]
            description = row[ledgerIndexes['Description']]

    msg = (f"""
The balance of {toAccount} is <:oddcoin:855612234558341161>{balance}<:oddcoin:855612234558341161>
From a {action} on {date} from {fromAccount}
For: {description}
    """)
    if not foundIt:
        msg = 'Did not find an account with that @ID'
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




# ~~~~~~~~~~~~~ ETH Functions ~~~~~~~~~~~~~
@bot.command()
async def eth(ctx):
    url = 'https://ethereumprice.org/'
    # html = urllib.request.urlopen(url)
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    ethPriceCurrency = soup.find('div', {'id':'coin-price'}).find('span',{'class':'currency-symbol'})
    ethPrice = soup.find('div', {'id':'coin-price'}).find('span',{'class':'value'})

    msg = (f'Eth is currently at {ethPriceCurrency.text}{ethPrice.text}')
    await ctx.send(msg)




# ~~~~~~~~~~~~~ Utility Functions ~~~~~~~~~~~~~
async def getWorkSheet():
    client = pygsheets.authorize(service_file=serviceAccountFile)
    sheet = client.open_by_key(GSHEETS_SPREADSHEET_URL_KEY)
    wks = sheet.worksheet_by_title('Sheet1')
    return wks

def getLabelIndexes(tableHeaders):
    # figure out what columns are the ones we want
    ledgerIndexes = {x:0 for x in ledgerColumns}
    for columnIndex, columnHeader in enumerate(tableHeaders):
        for labelString in ledgerIndexes:
            if columnHeader == labelString:
                ledgerIndexes[labelString] = columnIndex
    return ledgerIndexes













# ~~~~~~~~~~~~~ Example Command Functions ~~~~~~~~~~~~~

@bot.command()
async def thumb(ctx):
    await ctx.send('Send me that 👍 reaction, mate')
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) == '👍'

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('👎 Ahh for real')
    else:
        await ctx.send('👍 Thanks brah')


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
