"""Bot functions."""

import spotipy
import conf
import spotifyAPI


async def searchArtistGenre(artistName):
    """Return a list of music genre corresponding to the artistName."""
    spotify = spotipy.Spotify()
    results = spotify.search(q='artist:' + artistName, type='artist')

    try:
        return ', '.join(results['artists']['items'][0]['genres'])
    except:
        return "Sorry, artist not found!"

async def aboutMe():
    """Return various informations about the user."""
    results = await spotifyAPI.api_call("https://api.spotify.com/v1/me", conf.SPOTIFY_TOEKN)

    return "Id: " + results['id'] + \
           "\nEmail: " + results['email'] + \
           "\nBirthdate: " + results['birthdate'] + \
           "\nCountry: " + results['country'] + \
           "\nUri: " + results['uri']

async def currentlyPlaying():
    """Return which song is currently playing."""
    results = await spotifyAPI.api_call("https://api.spotify.com/v1/me/player/currently-playing", conf.SPOTIFY_TOEKN)

    if results['is_playing']:
        return "Artist: " + results['item']['album']['artists'][0]['name'] + \
               "\nAlbum cover: " + results['item']['album']['images'][0]['url']
    else:
        return "There is currently no music played."

async def remote_control(command):
    """Play, pause, next or previous"""
    method="PUT"
    if command in ('next', 'previous'):
        method = "POST"

    results = await spotifyAPI.api_call(f"https://api.spotify.com/v1/me/player/{command}", conf.SPOTIFY_TOEKN, method)
    return results

async def volume(level):
    """Set the volume for the user’s current playback device."""
    try:
        level = int(level)
        results = await spotifyAPI.api_call(f"https://api.spotify.com/v1/me/player/volume?volume_percent={level}", conf.SPOTIFY_TOEKN, "PUT")
        return results
    except:
        return "Please, enter a number between 0 and 100"

async def hlep():
    """Display all the avaiable commands."""
    resuts = "- about_me: \n" \
             "  Return various information about the user.\n\n" \
             "- currently_playing: \n" \
             "  Return informations about the music which is currently played.\n\n" \
             "- genre artistName: \n" \
             "  Return a list of music genre corresponding to the artistName. \n\n" \
             "- help: \n" \
             "  Display the help.\n\n" \
             "- remote_control play/pause/next/previous: \n" \
             "can play/pause the track, or go to the next/previous one of the playlist.\n\n" \
             "- volume level: \n" \
             "  Set the volume to level, with 0 <= level <= 100."

    return  resuts