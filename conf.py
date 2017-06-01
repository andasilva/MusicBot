"""Global configuration variables."""

import spotipy.util
import bot_functions

from selenium import webdriver


########################
#   GENERAL SETTINGS   #
########################

driver = webdriver.Chrome() # chromedriver in PATH / for Firefox:  webdriver.Firefox() (+ geckodriver)

#Dictionary for bot commands.
commands = {'about_me': bot_functions.aboutMe,
            'currently_playing': bot_functions.currentlyPlaying,
            'help': bot_functions.hlep,
            'pause': bot_functions.pause,
            'play': bot_functions.play,
            'remote_control': bot_functions.remote_control,
            'search': bot_functions.searchArtist,
            'skip': bot_functions.skip,
            'vol': bot_functions.vol,
            'volume': bot_functions.volume}


CHANNEL_ID = '...'


########################
#   DISCORD SETTINGS   #
########################

DISCORD_TOKEN = '...'


########################
#   SPOTIFY SETTINGS   #
########################

SPOTIFY_CLIENT_ID = '...'

SPOTIFY_CLIENT_SECRET = '...'

SPOTIFY_REDIRECT_URI = 'https://discordapp.com/channels/@me'

SPOTIFY_URL = f"https://accounts.spotify.com/authorize/?" \
              f"client_id={SPOTIFY_CLIENT_ID}&" \
              f"response_type=code&" \
              f"redirect_uri={SPOTIFY_REDIRECT_URI}&" \
              f"scope=user-read-birthdate%20user-read-private%20user-read-email%20user-read-currently-playing&" \
              f"state=34fFs29kd09"

SPOTIFY_SCOPE = 'user-read-birthdate user-read-private user-read-email user-read-currently-playing user-modify-playback-state'

SPOTIFY_TOKEN = spotipy.util.prompt_for_user_token('USERNAME', scope=SPOTIFY_SCOPE,
                                                   client_id=SPOTIFY_CLIENT_ID,
                                                   client_secret=SPOTIFY_CLIENT_SECRET,
                                                   redirect_uri=SPOTIFY_REDIRECT_URI)