# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 19:22:57 2025

@author: hrlov
These comments are for you Ale
"""

from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
import spotipy

# Load environment variables
load_dotenv()

# URLS can be found throughout https://developer.spotify.com/console/
AVAILABLE_DEVICES_URL = 'https://api.spotify.com/v1/me/player/devices'
SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'
NEXT_URL = 'https://api.spotify.com/v1/me/player/next'
PREVIOUS_URL = 'https://api.spotify.com/v1/me/player/previous'
PAUSE_URL = 'https://api.spotify.com/v1/me/player/pause'
PLAY_URL = 'https://api.spotify.com/v1/me/player/play'
SAVED_TRACKS = 'https://api.spotify.com/v1/me/tracks'
VOLUME = 'https://api.spotify.com/v1/me/player/volume'
SPOTIPY_REDIRECT_URI="http://127.0.0.1:8888/callback"

# Get the authentication token for Spotify using Client Authorization Code Flow
scope = "user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-recently-played"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# 🎵 Get the current device Spotify is playing on
def get_device():
    devices = sp.devices()
    if "devices" not in devices:
        print("Error: 'devices' key missing from response.")
        return None  # Handle missing key gracefully

    for device in devices["devices"]:
        if device["is_active"]:
            return device["id"]

    print("No active device found.")
    return None  # No active device found

        
# Checks which device is currently being used by spotify
DEVICE_ID = get_device() 

# 🎶 Get the currently playing track
def get_current_track():
    current_track = sp.current_playback()
    if not current_track or "item" not in current_track:
        print("No track is currently playing.")
        return None

    track = current_track["item"]
    track_name = track["name"]
    artists = ", ".join([artist["name"] for artist in track["artists"]])
    link = track["external_urls"]["spotify"]

    return {
        "Title": track_name,
        "Artist(s)": artists,
        "Link": link,
    }

# 🎶 Get the previously played track
def get_previous_track():
    results = sp.current_user_recently_played(limit=1)  # Get the last played track
    if not results or "items" not in results or len(results["items"]) == 0:
        print("No previously played track found.")
        return None

    track = results["items"][0]["track"]
    track_name = track["name"]
    artists = ", ".join([artist["name"] for artist in track["artists"]])
    link = track["external_urls"]["spotify"]

    return {
        "Title": track_name,
        "Artist(s)": artists,
        "Link": link,
    }

def save():
    return

# 🔀 Playback Controls
def next_track():
    sp.next_track(device_id=DEVICE_ID)

def previous_track():
    sp.previous_track(device_id=DEVICE_ID)

def pause():
    sp.pause_playback(device_id=DEVICE_ID)

def play():
    sp.start_playback(device_id=DEVICE_ID)