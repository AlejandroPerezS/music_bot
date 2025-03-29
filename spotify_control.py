# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 19:22:57 2025

@author: hrlov
"""

from dotenv import load_dotenv
from requests import post
import os
import base64
import json

# Load environment variables
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# URLS can be found throughout https://developer.spotify.com/console/

# SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'
# NEXT_URL = 'https://api.spotify.com/v1/me/player/next'
# PREVIOUS_URL = 'https://api.spotify.com/v1/me/player/previous'
# PAUSE_URL = 'https://api.spotify.com/v1/me/player/pause'
# PLAY_URL = 'https://api.spotify.com/v1/me/player/play'
# RECENT_TRACKS = 'https://api.spotify.com/v1/me/player/recently-played'
# SAVED_TRACKS = 'https://api.spotify.com/v1/me/tracks'
# VOLUME = 'https://api.spotify.com/v1/me/player/volume'
# TOP = '	https://api.spotify.com/v1/me/top/'
# USER_PLAYLISTS = 'https://api.spotify.com/v1/me/playlists'

# Get the authentication token of the Spotify App
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
        }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

# Make the token viable
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

token = get_token()