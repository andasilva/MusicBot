"""Global configuration variables."""

import spotipy.util


########################
#   GENERAL SETTINGS   #
########################

driver = None

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