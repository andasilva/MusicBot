"""Bot functions."""

import conf
import json


async def searchArtist(spotify_client, artistName):
    """Return various informations about the artist searched."""

    try:
        json.loads(artistName) # Make sure we found an artist

        artistName = artistName.replace(" ", "%20")
        results = await spotify_client.api_call(f"/search?q={artistName}&type=artist")

        return "Artist: " + results['artists']['items'][0]['name'] + "\n" \
               "Genre: " + ''.join(results['artists']['items'][0]['genres']) + \
               "\n" + results['artists']['items'][0]['images'][0]['url']
    except:
        return "Sorry, artist not found!"

async def aboutMe(spotify_client):
    """Return various informations about the user."""
    results = await spotify_client.api_call("/me")

    return "Id: " + results['id'] + \
           "\nEmail: " + results['email'] + \
           "\nBirthdate: " + results['birthdate'] + \
           "\nCountry: " + results['country'] + \
           "\nUri: " + results['uri']


async def currentlyPlaying(spotify_client):
    """Return which song is currently playing."""
    results = await spotify_client.api_call("/me/player/currently-playing")

    if results['is_playing']:
        return "Artist: " + results['item']['album']['artists'][0]['name'] + "\n" \
               "Title: " + results['item']['name'] + \
               "\nAlbum cover: " + results['item']['album']['images'][0]['url']
    else:
        return "There is currently no music played."


async def play(spotify_client):
    """Play for non premium users."""
    if await currentlyPlaying(spotify_client) != "There is currently no music played.":
        return "Music's already playing."

    return playPause('play')


async def pause(spotify_client):
    """Pause for non premium users."""
    if await currentlyPlaying(spotify_client) == "There is currently no music played.":
        return "Music's already paused."

    return playPause('pause')


def playPause(command):
    """Start/Stop the music."""
    playPause = conf.driver.find_element_by_class_name(f"spoticon-{command}-16")
    playPause.click()
    return {}


async def skip(spotify_client, command):
    """Skip back/forward for non premium users."""
    try:
        skip = conf.driver.find_element_by_class_name(f"spoticon-skip-{command}-16")
        skip.click()
        if command == 'back':
            skip.click() # one clik only restart the current music
        return {}
    except:
        return "Sorry, the only args avaiable for 'skip' are 'back' and 'forward'"


async def vol(spotify_client, level):
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

async def remote_control(spotify_client, command):
    """Play, pause, next or previous"""
    method = None
    if command in ('next', 'previous'):
        method = "POST"
    else:
        method = "PUT"

    results = await spotify_client.api_call(f"/me/player/{command}", method)
    return results


async def volume(spotify_client, level):
    """Set the volume for the user’s current playback device."""
    try:
        level = int(level)
        results = await spotify_client.api_call(f"/me/player/volume?volume_percent={level}", "PUT")
        return results
    except:
        return "Please, enter a number between 0 and 100"


############
#   HELP   #
############

async def hlep(*args):
    """Display all the avaiable commands."""

    results = """
    ```- about_me: \n
    Return various information about the user.```
    ```- currently_playing: \n
    Return informations about the music which is currently played.```
    ```- help: \n
      Display the help.```
    ```- search artistName: \n
    Return various informations about the artist searched.``` 
    ```- skip back/forward: \n
      Can go to the next/previous track of the playlist without a Spotify premium account.``` 
    ```- pause: \n
      Can pause the track without a Spotify premium account.``` 
    ```- play: \n
      Can play the track without a Spotify premium account.``` 
    ```- vol level: \n
      Set the volume to level without a Spotify premium account, with 0 <= level <= 100.``` 
    **---------- SPOTIFY PREMIUM ACCOUNT REQUIRED ----------**
    ```- remote_control play/pause/next/previous: \n
      can play/pause the track, or go to the next/previous one of the playlist.```
    ```- volume level: \n
      Set the volume to level, with 0 <= level <= 100.```"""
    return results