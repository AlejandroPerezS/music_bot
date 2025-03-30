# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 19:22:57 2025

@author: AlejandroPerezS, Huntyboy102
"""
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import spotify_control as spc
from deezer import search_deezer
import youtube_logic


# Load environment variables because GitHub doesn't inject shit lol
load_dotenv()

# Create intents
intents = discord.Intents.default()
intents.message_content = True

# Get the token directly from environment (GitHub will inject it (No it won't))
TOKEN = os.getenv("DISCORD_TOKEN")


# Create easy to use commands instead of stacking them in on_message function
# this is from the discord.ext library
bot = commands.Bot(command_prefix='$', intents=intents)

# this runs on ap start
@bot.event
async def on_ready():
     print('Bot logged in as {0.user}'.format(bot))


# LOTS OF cool stuff
# basically just join th bot to a channel
@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if len(channel.members) > 0:
            if not ctx.voice_client:
                await channel.connect()
                print(f"Bot joined {channel.name}")
            elif ctx.voice_client.channel != channel:
                await ctx.voice_client.move_to(channel)
                print(f"Bot moved to {channel.name}")
        else:
            await ctx.send("No members are in this channel.")
    else:
        await ctx.send("You need to join a voice channel first.")


#########################
# youtube
# Command to play a song from YouTube
@bot.command()
async def play(ctx, url: str):
    await youtube_logic.play_song(ctx, url)



########################
#deezer
@bot.command()
async def deezer_search(ctx,*,song):
    result = search_deezer(song)
    if result:
        track_name , artist_name, track_url = result
        await ctx.send(f"Found: {track_name} by {artist_name}\nListen here: {track_url}")
    else:
        await ctx.send("No results found.")





####################################
# Spotifty
@bot.command()
async def spotify(ctx):
    await ctx.send('I am capable of using the following spotify commands.'
                               '\n[$current_song] Get the currently playing track.'
                               '\n[$previous_song] Get the previously playing track.'
                               '\n[$next_song] Play the next song in queue.'
                               '\n[$previous] Play the previous song'
                               '\n[$pause] Pause the currently playing song'
                               '\n[$spotify_play] Play the currently paused song'
                               '\n[$queue] Add song to queue.'
                               '\n[$save] Save the current song to "Liked Songs"')

@bot.command()
async def current_song(ctx):
    current_track = spc.get_current_track()
    await ctx.send("The current track is: " + str(current_track))
    
@bot.command()
async def previous_song(ctx):
    previous_track = spc.get_previous_track()
    await ctx.send("The previous track was: " + str(previous_track))
    
@bot.command()
async def next_song(ctx):
    spc.next_track()
    await ctx.send("Skipped track.")
    
@bot.command()
async def previous(ctx):
    spc.previous_track()
    await ctx.send("Going to previous track.")
    
@bot.command()
async def pause(ctx):
    spc.pause()
    await ctx.send("Track paused.")
    
@bot.command()
async def spotify_play(ctx):
    spc.play()
    await ctx.send("Track resumed.")
    
@bot.command()
async def queue(ctx):
    return
    
@bot.command()
async def add(ctx):
    return

bot.run(TOKEN)