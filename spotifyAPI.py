"""Spotify API tools."""

import spotipy


def searchArtistStyle(name):
    spotify = spotipy.Spotify()
    results = spotify.search(q='artist:' + name, type='artist')
    print(results)
    return results['artists']['items'][0]['genres']