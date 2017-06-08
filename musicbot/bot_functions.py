"""Bot functions."""

from urllib.parse import urlencode

from selenium import webdriver

from . import settings
from .conf import reset_config


async def reset(*args):
    """Reset bot settings."""
    reset_config()
    return "Settings reset. Reboot the bot to configure the settings."


async def search_artist(*args):
    """Return various informations about the artist searched."""
    spotify_client = args[0]
    artistName = args[1]

    url = urlencode(
        {"q": artistName, "type": "artist"},
        doseq=True,
        encoding='utf-8'
    )

    results = await spotify_client.api_call(
        f"/search?{url}"
    )

    if results['artists']['items'] != []:
        return "Artist: " + results['artists']['items'][0]['name'] + "\n" \
           "Genre: " + ''.join(results['artists']['items'][0]['genres']) + \
           "\n" + results['artists']['items'][0]['images'][0]['url']

    return "Sorry, artist not found!"


async def about_me(*args):
    """Return various informations about the user."""
    spotify_client = args[0]
    results = await spotify_client.api_call("/me")

    return "Id: " + results['id'] + \
           "\nEmail: " + results['email'] + \
           "\nBirthdate: " + results['birthdate'] + \
           "\nCountry: " + results['country'] + \
           "\nUri: " + results['uri']


async def currently_playing(*args):
    """Return which song is currently playing."""
    spotify_client = args[0]
    results = await spotify_client.api_call("/me/player/currently-playing")

    if results['is_playing']:
        return "Artist: " + \
               results['item']['album']['artists'][0]['name'] + \
               "\n" \
               "Title: " + results['item']['name'] + \
               "\nAlbum cover: " + \
               results['item']['album']['images'][0]['url']
    else:
        return "There is currently no music played."


async def play(*args):
    """Play for non premium users."""
    spotify_client = args[0]
    if (await currently_playing(spotify_client) !=
            "There is currently no music played."):
        return "Music's already playing."

    return play_pause('play')


async def pause(*args):
    """Pause for non premium users."""
    spotify_client = args[0]
    if (await currently_playing(spotify_client) ==
            "There is currently no music played."):
        return "Music's already paused."

    return play_pause('pause')


def play_pause(command):
    """Start/Stop the music."""
    if is_driver_running() is True:
        playPause = settings.driver.find_element_by_class_name(
            f"spoticon-{command}-16")
        playPause.click()
        return {}
    return "Please, start the webdriver with " \
           "the following command: ```open_spotify```" \
           "and login to spotify"


async def skip(*args):
    """Skip back/forward for non premium users."""
    command = args[1]
    if is_driver_running() is True:
        try:
            print(*args)
            skip = settings.driver.find_element_by_class_name(
                f"spoticon-skip-{command}-16"
            )
            skip.click()
            if command == 'back':
                skip.click()  # one clik only restart the current music
            return {}
        except Exception:
            return "Sorry, the only args avaiable for " \
                   "'skip' are 'back' and 'forward'"
    return "Please, start the webdriver with " \
           "the following command: ```open_spotify```"


async def vol(*args):
    """Set the  volume for non premium users."""
    level = args[1]
    if is_driver_running() is True:
        try:
            level = int(level)
            assert 0 <= level <= 100
            volume = settings.driver.find_elements_by_class_name(
                "progress-bar__fg"
            )[1]
            actions = settings.webdriver.\
                ActionChains(settings.driver)
            actions.move_to_element_with_offset(volume, level, 0)
            actions.click()
            actions.perform()
            return {}
        except Exception:
            return "Please, enter a number between 0 and 100"
    return "Please, start the webdriver with " \
           "the following command: ```open_spotify```"


######################################
#  SPOTIFY PREMIUM ACCOUNT REQUIRED  #
######################################

async def remote_control(*args):
    """Play, pause, next or previous."""
    spotify_client = args[0]
    command = args[1]

    method = None
    if command in ('next', 'previous'):
        method = "POST"
    else:
        method = "PUT"

    results = await spotify_client.api_call(f"/me/player/{command}", method)
    return results


async def volume(*args):
    """Set the volume for the user’s current playback device."""
    spotify_client = args[0]
    level = args[1]
    try:
        level = int(level)
        results = await spotify_client.api_call(
            f"/me/player/volume?volume_percent={level}",
            "PUT"
        )
        return results
    except Exception:
        return "Please, enter a number between 0 and 100"


############
#   HELP   #
############

async def help(*args):
    """Display all the avaiable commands."""
    results = """
    ```- about_me:
    Return various information about the user.```
    ```- reset:
    Reconfigure application settings (bot reboot required).```
    ```- currently_playing:
    Return informations about the music which is currently played.```
    ```- help:
      Display the help.```
    ```- search_artist artistName:
    Return various informations about the artist searched.```
    ```- skip back/forward:
      Can go to the next/previous track of the
      playlist without a Spotify premium account.```
    ```- pause:
      Can pause the track without a Spotify premium account.```
    ```- play:
      Can play the track without a Spotify premium account.```
    ```- vol level:
      Set the volume to level without a Spotify premium
      account, with 0 <= level <= 100.```
    **---------- SPOTIFY PREMIUM ACCOUNT REQUIRED ----------**
    ```- remote_control play/pause/next/previous:
      can play/pause the track, or go to
      the next/previous one of the playlist.```
    ```- volume level:
      Set the volume to level, with 0 <= level <= 100.```"""
    return results


################
#  WEB DRIVER  #
################

async def open_spotify(*args):
    """Start a webdriver and go on Spotify wepage."""
    # chromedriver in PATH / for Firefox:  webdriver.Firefox() (+ geckodriver)
    settings.driver = webdriver.Chrome()
    settings.driver.get("https://open.spotify.com/browse/featured")

    hasAccount = settings.driver.find_element_by_id('has-account')
    hasAccount.click()

    loginUsr = settings.driver.find_element_by_id('login-usr')
    loginUsr.clear()
    loginUsr.send_keys("")  # Optional

    loginPass = settings.driver.find_element_by_id('login-pass')
    loginPass.clear()
    loginPass.send_keys("")  # Optional

    return "Spotify started, let's log you."


def is_driver_running():
    """Check if the driver is running."""
    return settings.driver is not None
