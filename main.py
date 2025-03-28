import discord
import os
# intents are needed for teh client section
# so here we add if this supposed to message join chat and more
# Create intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent if needed

# loading the .env token since there is a bug
TOKEN = os.getenv("DISCORD_TOKEN")

# discord bots listen for event and then reacts to it
client = discord.Client(intents=intents)
#log in event
@client.event
async def on_ready():
    print('Bot logged in as {0.user}'.format(client))
#on message even
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(TOKEN)