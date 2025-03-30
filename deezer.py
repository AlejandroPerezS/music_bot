# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 2254 2025

@author: AlejandroPerezS
"""

import requests

def search_deezer(query):
    query = query.replace(' ', '+')

    url = f'https://api.deezer.com/search?q={query}'

    response = requests.get(url)
    data = response.json()


    if data['total'] > 0:
        track = data['data'][0]
        track_name = track['title']
        artist_name = track['artist']['name']
        track_url = track['link']
        return track_name, artist_name, track_url
    else:
        return None