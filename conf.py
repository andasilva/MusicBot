"""Global configuration variables."""

import spotipy.util
import botFunctions

from selenium import webdriver


########################
#   GENERAL SETTINGS   #
########################

driver = webdriver.Chrome() # chromedriver in PATH / for Firefox:  webdriver.Firefox() (+ geckodriver)

#Dictionary for bot commands.
commands = {'about_me': botFunctions.aboutMe,
            'currently_playing': botFunctions.currentlyPlaying,
            'genre': botFunctions.searchArtistGenre,
            'help': botFunctions.hlep,
            'pause': botFunctions.pause,
            'play': botFunctions.play,
            'remote_control': botFunctions.remote_control,
            'skip': botFunctions.skip,
            'vol': botFunctions.vol,
            'volume': botFunctions.volume}


########################
#   DISCORD SETTINGS   #
########################

DISCORD_URL = "https://discordapp.com/api"
"""Discord HTTP API endpoint."""

DISCORD_TOKEN = ...

DISCORD_HEADER = {
    "headers": {
        "Authorization": f"Bot {DISCORD_TOKEN}",
        "User-Agent": "DiscordBot (http://he-arc.ch/, 0.1)"
    }
}


########################
#   SPOTIFY SETTINGS   #
########################

SPOTIFY_CLIENT_ID = ...

SPOTIFY_CLIENT_SECRET = ...

SPOTIFY_REDIRECT_URI = 'https://discordapp.com/channels/@me'

SPOTIFY_URL = f"https://accounts.spotify.com/authorize/?" \
              f"client_id={SPOTIFY_CLIENT_ID}&" \
              f"response_type=code&" \
              f"redirect_uri={SPOTIFY_REDIRECT_URI}&" \
              f"scope=user-read-birthdate%20user-read-private%20user-read-email%20user-read-currently-playing&" \
              f"state=34fFs29kd09"

SPOTIFY_SCOPE = 'user-read-birthdate user-read-private user-read-email user-read-currently-playing user-modify-playback-state'

SPOTIFY_TOEKN = spotipy.util.prompt_for_user_token('SPOTIFY USERNAME', scope=SPOTIFY_SCOPE,
                                                   client_id=SPOTIFY_CLIENT_ID,
                                                   client_secret=SPOTIFY_CLIENT_SECRET,
                                                   redirect_uri=SPOTIFY_REDIRECT_URI)

SPOTIFY_HEADER = {
    "headers": {
        "Authorization": f"Bearer {SPOTIFY_TOEKN}",
        "User-Agent": "DiscordBot (http://he-arc.ch/, 0.1)"
    }
}