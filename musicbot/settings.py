"""Global configuration variables."""

########################
#   GENERAL SETTINGS   #
########################

driver = None

CHANNEL_ID = ''

########################
#   DISCORD SETTINGS   #
########################

DISCORD_TOKEN = ''
########################
#   SPOTIFY SETTINGS   #
########################

S_CLIENT_ID = ''
S_CLIENT_SECRET = ''
S_REDIRECT_URI = 'https://discordapp.com/channels/@me'

S_URL = f"https://accounts.spotify.com/authorize/?" \
        f"client_id={S_CLIENT_ID}&" \
        f"response_type=code&" \
        f"redirect_uri={S_REDIRECT_URI}&" \
        f"scope=user-read-birthdate%20user-read-private%20" \
        f"user-read-email%20user-read-currently-playing&" \
        f"state=34fFs29kd09"

S_SCOPE = """user-read-birthdate
             user-read-private
             user-read-email
             user-read-currently-playing
             user-modify-playback-state"""

S_TOKEN = ''
