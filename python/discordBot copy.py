
import discord


client = discord.Client()

@client.event
async def on_ready():
    print("The bot is ready!")
    await client.change_presence(game=discord.Game(name="Making a bot"))




@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == "Hello":
        await client.send_message(message.channel, "World")






client.run("NjY5NzA4ODUyMTQ4NTY4MDY0.Xijw-A.oTY4VSX46XaQGmj5MCsRyT6z52E")
# client.run("https://discord.com/api/oauth2/authorize?client_id=669708852148568064&permissions=134144&scope=bot")

