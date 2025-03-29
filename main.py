# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 19:22:57 2025

@author: AlejandroPerezS, Huntyboy102
"""

import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables because Github doesn't inject shit
load_dotenv()

# Create intents
intents = discord.Intents.default()
intents.message_content = True

# Get the token directly from environment (GitHub will inject it (No it won't))
TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client(intents=intents)

# Create easy to use commands instead of stacking them in on_message function
bot = commands.Bot(command_prefix='$', intents=intents)

@client.event
async def on_ready():
    print('Bot logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
        
    # Help commands for spotify
    if message.content.startswith('$spotify'):
        await message.channel.send('I am capable of using the following spotify commands.'
                                   '\n[$sp_get_current] Get the currently playing track.'
                                   '\n[$sp_get_previous] Get the previously playing track.'
                                   '\n[$sp_next] Play the next song in queue.'
                                   '\n[$sp_previous] Play the previous song'
                                   '\n[$sp_pause] Pause the currently playing song'
                                   '\n[$sp_play] Play the currently paused song'
                                   '\n[$sp_queue] Add song to queue.'
                                   '\n[$sp_save] Save the current song to "Liked Songs"')
@bot.command()
async def spotify_previous(ctx, *, arg):
    await ctx.send("Fuck you")
    
client.run(TOKEN)