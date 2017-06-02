"""Bot functions."""

from selenium import webdriver


async def searchArtist(artistName, spotify_client):
    """Return various informations about the artist searched."""
    results = await spotify_client.api_call(
        f"/search?q={artistName}&type=artist")

    if results['artists']['items'] != []:
        return "Artist: " + results['artists']['items'][0]['name'] + "\n" \
           "Genre: " + ''.join(results['artists']['items'][0]['genres']) + \
           "\n" + results['artists']['items'][0]['images'][0]['url']

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
        return "Artist: " + \
               results['item']['album']['artists'][0]['name'] + \
               "\n" \
               "Title: " + results['item']['name'] + \
               "\nAlbum cover: " + \
               results['item']['album']['images'][0]['url']
    else:
        return "There is currently no music played."


async def play(spotify_client):
    """Play for non premium users."""
    if await (currentlyPlaying(spotify_client) !=
              "There is currently no music played."):
        return "Music's already playing."

    return playPause('play')


async def pause(spotify_client):
    """Pause for non premium users."""
    if await (currentlyPlaying(spotify_client) ==
              "There is currently no music played."):
        return "Music's already paused."

    return playPause('pause')


def playPause(command):
    """Start/Stop the music."""
    if isDriverRunning() is True:
        playPause = conf.driver.find_element_by_class_name(
            f"spoticon-{command}-16")
        playPause.click()
        return {}
    return isDriverRunning()


async def skip(command, *args):
    """Skip back/forward for non premium users."""
    if isDriverRunning() is True:
        try:
            skip = conf.driver.find_element_by_class_name(
                f"spoticon-skip-{command}-16")
            skip.click()
            if command == 'back':
                skip.click()  # one clik only restart the current music
            return {}
        except Exception:
            return """"Sorry, the only args avaiable for
                       'skip' are 'back' and 'forward'"""
    return isDriverRunning()


async def vol(level, *args):
    """Set the  volume for non premium users."""
    if isDriverRunning() is True:
        try:
            level = int(level)
            assert 0 <= level <= 100
            volume = conf.driver.find_elements_by_class_name(
                "progress-bar__fg")[1]
            actions = conf.webdriver.ActionChains(conf.driver)
            actions.move_to_element_with_offset(volume, level, 0)
            actions.click()
            actions.perform()
            return {}
        except Exception:
            return "Please, enter a number between 0 and 100"
    return isDriverRunning()


######################################
#  SPOTIFY PREMIUM ACCOUNT REQUIRED  #
######################################

async def remote_control(command, spotify_client):
    """Play, pause, next or previous."""
    method = None
    if command in ('next', 'previous'):
        method = "POST"
    else:
        method = "PUT"

    results = await spotify_client.api_call(f"/me/player/{command}", method)
    return results


async def volume(level, spotify_client):
    """Set the volume for the user’s current playback device."""
    try:
        level = int(level)
        results = await spotify_client.api_call(
            f"/me/player/volume?volume_percent={level}",
            "PUT")
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
    ```- currently_playing:
    Return informations about the music which is currently played.```
    ```- help:
      Display the help.```
    ```- search artistName:
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

async def openSpotify(*args):
    """Start a webdriver and go on Spotify wepage."""
    # chromedriver in PATH / for Firefox:  webdriver.Firefox() (+ geckodriver)
    conf.driver = webdriver.Chrome()
    conf.driver.get("https://open.spotify.com/browse/featured")

    hasAccount = conf.driver.find_element_by_id('has-account')
    hasAccount.click()

    loginUsr = conf.driver.find_element_by_id('login-usr')
    loginUsr.clear()
    loginUsr.send_keys("")  # Optional

    loginPass = conf.driver.find_element_by_id('login-pass')
    loginPass.clear()
    loginPass.send_keys("")  # Optional

    return {}


def isDriverRunning():
    """Check if the driver is running."""
    if conf.driver is not None:
        return True
    return """Please, start the webdriver with
              the following command: ```open_spotify```"""
