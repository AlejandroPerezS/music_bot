# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 19:22:57 2025

@author: AlejandroPerezS, Huntyboy102
"""

from discord.ext import commands
from dotenv import load_dotenv
import discord
import os
import spotify_control as spc

# Load environment variables because Github doesn't inject shit
load_dotenv()

# Create intents
intents = discord.Intents.default()
intents.message_content = True

# Get the token directly from environment (GitHub will inject it (No it won't))
TOKEN = os.getenv("DISCORD_TOKEN")

# Create easy to use commands instead of stacking them in on_message function
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
     print('Bot logged in as {0.user}'.format(bot))

@bot.command()
async def spotify(ctx):
    await ctx.send('I am capable of using the following spotify commands.'
                               '\n[$sp_get_current] Get the currently playing track.'
                               '\n[$sp_get_previous] Get the previously playing track.'
                               '\n[$sp_next] Play the next song in queue.'
                               '\n[$sp_previous] Play the previous song'
                               '\n[$sp_pause] Pause the currently playing song'
                               '\n[$sp_play] Play the currently paused song'
                               '\n[$sp_queue] Add song to queue.'
                               '\n[$sp_save] Save the current song to "Liked Songs"')
        
@bot.command()
async def sp_get_current(ctx):
    current_track = spc.get_current_track()
    await ctx.send("The current track is: " + str(current_track))
    
@bot.command()
async def sp_get_previous(ctx):
    previous_track = spc.get_previous_track()
    await ctx.send("The previous track was: " + str(previous_track))
    
@bot.command()
async def sp_next(ctx):
    spc.next_track()
    await ctx.send("Skipped track.")
    
@bot.command()
async def sp_previous(ctx):
    spc.previous_track()
    await ctx.send("Going to previous track.")
    
@bot.command()
async def sp_pause(ctx):
    spc.pause()
    await ctx.send("Track paused.")
    
@bot.command()
async def sp_play(ctx):
    spc.play()
    await ctx.send("Track resumed.")
    
@bot.command()
async def sp_queue(ctx):
    return
    
@bot.command()
async def sp_add(ctx):
    return

bot.run(TOKEN)