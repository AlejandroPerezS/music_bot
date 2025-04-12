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
            'format': 'bestaudio/best',
            'quiet': True,
        }

        with ytdlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)

            for fmt in info_dict['formats']:
                # We want non-HLS audio-only streams
                if (
                    fmt.get('acodec') != 'none' and
                    fmt.get('vcodec') == 'none' and
                    not fmt['url'].endswith('.m3u8')
                ):
                    return fmt['url']

            print("No valid direct audio stream found.")
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

    print(f"Attempting to play audio URL: {audio_url}")

    # Ensure the bot is connected to a voice channel
    if not ctx.voice_client:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await ctx.send("You need to join a voice channel first.")
            return

    voice_client = ctx.voice_client

    # Play the audio with FFmpeg
    ffmpeg_options = {
        'options': '-vn'
    }

    def after_playback(error):
        if error:
            print(f"Playback error: {error}")

    voice_client.play(discord.FFmpegPCMAudio(audio_url, **ffmpeg_options), after=after_playback)

    # Wait for audio to start (up to 5 seconds)
    for _ in range(10):
        if voice_client.is_playing():
            break
        await asyncio.sleep(0.5)

    if not voice_client.is_playing():
        await ctx.send("Something went wrong. The audio failed to start.")
        await voice_client.disconnect()
        return

    await ctx.send(f"Now playing: {song_name}")

    # Wait until it finishes
    while voice_client.is_playing():
        await asyncio.sleep(1)

    await voice_client.disconnect()
