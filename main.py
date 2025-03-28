import discord
import os

# Create intents
intents = discord.Intents.default()
intents.message_content = True

# Get the token directly from environment (GitHub will inject it)
TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Bot logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(TOKEN)

