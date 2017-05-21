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
    token = conf.getSpotifyToken('user-read-birthdate user-read-private user-read-email')

    results = await spotifyAPI.api_call("https://api.spotify.com/v1/me", token)

    return "Id: " + results['id'] + \
           "\nEmail: " + results['email'] + \
           "\nBirthdate: " + results['birthdate'] + \
           "\nCountry: " + results['country'] + \
           "\nUri: " + results['uri']

async def currentlyPlaying():
    """Return which song is currently playing."""
    token = conf.getSpotifyToken('user-read-currently-playing')

    results = await spotifyAPI.api_call("https://api.spotify.com/v1/me/player/currently-playing", token)

    if results['is_playing']:
        return "Artist: " + results['item']['album']['artists'][0]['name'] + \
               "\nAlbum cover: " + results['item']['album']['images'][0]['url']
    else:
        return "There is currently no music played."

async def hlep():
    """Display all the avaiable commands."""
    resuts = "- currently_playing: \n" \
             "Return informations about the music which is currently played\n\n" \
             "- genre artistName: \n" \
             "  Return a list of music genre corresponding to the artistName. \n\n" \
             "- about_me: \n" \
             "  Return various information about the user."
    return  resuts