"""Bot functions."""

import spotipy
import APIs
import conf


async def searchArtistGenre(artistName):
    """Return a list of music genre corresponding to the artistName."""
    if artistName == '':
        return "You must enter an artist name!"

    spotify = spotipy.Spotify()
    results = spotify.search(q='artist:' + artistName, type='artist')

    try:
        return ', '.join(results['artists']['items'][0]['genres'])
    except:
        return "Sorry, artist not found!"


async def aboutMe():
    """Return various informations about the user."""
    results = await APIs.api_call("https://api.spotify.com/v1/me", conf.SPOTIFY_HEADER)

    return "Id: " + results['id'] + \
           "\nEmail: " + results['email'] + \
           "\nBirthdate: " + results['birthdate'] + \
           "\nCountry: " + results['country'] + \
           "\nUri: " + results['uri']


async def currentlyPlaying():
    """Return which song is currently playing."""
    results = await APIs.api_call("https://api.spotify.com/v1/me/player/currently-playing", conf.SPOTIFY_HEADER)

    if results['is_playing']:
        return "Artist: " + results['item']['album']['artists'][0]['name'] + \
               "\nAlbum cover: " + results['item']['album']['images'][0]['url']
    else:
        return "There is currently no music played."


async def play():
    """Play for non premium users."""
    if await currentlyPlaying() != "There is currently no music played.":
        return "Music's already playing."

    return playPause('play')


async def pause():
    """Pause for non premium users."""
    if await currentlyPlaying() == "There is currently no music played.":
        return "Music's already paused."

    return playPause('pause')


def playPause(command):
    """Start/Stop the music."""
    playPause = conf.driver.find_element_by_class_name(f"spoticon-{command}-16")
    playPause.click()
    return {}


async def skip(command):
    """Skip back/forward for non premium users."""
    try:
        skip = conf.driver.find_element_by_class_name(f"spoticon-skip-{command}-16")
        skip.click()
        if command == 'back':
            skip.click() # one clik only restart the current music
        return {}
    except:
        return "Sorry, the only args avaiable for 'skip' are 'back' and 'forward'"


async def vol(level):
    """Set the  volume for non premium users."""
    try:
        level = int(level)
        assert 0 <= level <= 100
        volume = conf.driver.find_elements_by_class_name("progress-bar__fg")[1]
        actions = conf.webdriver.ActionChains(conf.driver)
        actions.move_to_element_with_offset(volume, level, 0)
        actions.click()
        actions.perform()
        return {}
    except:
        return "Please, enter a number between 0 and 100"


######################################
#  SPOTIFY PREMIUM ACCOUNT REQUIRED  #
######################################

async def remote_control(command):
    """Play, pause, next or previous"""
    method="PUT"
    if command in ('next', 'previous'):
        method = "POST"

    results = await APIs.api_call(f"https://api.spotify.com/v1/me/player/{command}", conf.SPOTIFY_HEADER, method)
    return results


async def volume(level):
    """Set the volume for the user’s current playback device."""
    try:
        level = int(level)
        results = await APIs.api_call(f"https://api.spotify.com/v1/me/player/volume?volume_percent={level}", conf.SPOTIFY_HEADER, "PUT")
        return results
    except:
        return "Please, enter a number between 0 and 100"


############
#   HELP   #
############

async def hlep():
    """Display all the avaiable commands."""

    results = """- about_me: \n
                Return various information about the user.\n\n
              - currently_playing: \n
                Return informations about the music which is currently played.\n\n
              - genre artistName: \n
                Return a list of music genre corresponding to the artistName. \n\n
              - help: \n
                Display the help.\n\n
              - skip back/forward: \n
                Can go to the next/previous track of the playlist without a Spotify premium account \n\n
              - pause: \n
                Can pause the track without a Spotify premium account. \n\n
              - play: \n
               Can play the track without a Spotify premium account. \n\n
              - vol level: \n
               Set the volume to level without a Spotify premium account, with 0 <= level <= 100. \n\n
              ------ SPOTIFY PREMIUM ACCOUNT REQUIRED ------\n\n
              - remote_control play/pause/next/previous: \n
              can play/pause the track, or go to the next/previous one of the playlist.\n\n
              - volume level: \n
                Set the volume to level, with 0 <= level <= 100."""
    return results