import yt_dlp as ytdlp
import discord
import asyncio
from googleapiclient.discovery import build
import os

# Load the YouTube token directly from environment
YOUTUBE_TOKEN = os.getenv("YOUTUBE")
youtube = build('youtube', 'v3', developerKey=YOUTUBE_TOKEN)

# Function to search YouTube for a song and return its URL
def search_youtube(query, youtube):
    try:
        request = youtube.search().list(
            part="snippet",
            q=query,
            type="video",
            order="relevance",
            maxResults=1
        )
        response = request.execute()

        if response['items']:
            video_id = response['items'][0]['id']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            return video_url
        return None
    except Exception as e:
        print(f"Error searching YouTube: {e}")
        return None

# Function to get the audio URL from the YouTube URL
def get_audio_url(url):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',  # Select best audio format
            'quiet': True,  # Suppress logs
            'outtmpl': '%(id)s.%(ext)s',  # Output template for downloaded file
            'postprocessors': [{
                'key': 'FFmpegAudioConvertor',  # Corrected to 'FFmpegAudioConvertor'
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with ytdlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            audio_url = info_dict['formats'][0]['url']
            return audio_url
    except Exception as e:
        print(f"Error extracting audio URL: {e}")
        return None

# Function to play a song using the YouTube URL
async def play_song(ctx, song_name):
    youtube_url = search_youtube(song_name, youtube)
    if not youtube_url:
        await ctx.send("Song not found.")
        return

    audio_url = get_audio_url(youtube_url)

    if not audio_url:
        await ctx.send("Error retrieving audio URL. Please try again later.")
        return

    # Ensure the bot is connected to a voice channel
    if not ctx.voice_client:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await ctx.send("You need to join a voice channel first.")
            return

    voice_client = ctx.voice_client

    # Play the audio in the voice channel
    voice_client.play(discord.FFmpegPCMAudio(audio_url))

    await ctx.send(f"Now playing: {song_name}")

    # Wait for the song to finish playing before disconnecting
    while voice_client.is_playing():
        await asyncio.sleep(1)

    await voice_client.disconnect()
