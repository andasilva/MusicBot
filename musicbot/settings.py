"""Global configuration variables."""

########################
#   GENERAL SETTINGS   #
########################

driver = None

CHANNEL_ID = '314731498622156801'

########################
#   DISCORD SETTINGS   #
########################

DISCORD_TOKEN = 'MzEyMTcwNjk2MTQ5MTcyMjI1.C_79Dg.sNdHiMqcsPkVZ3c83uxwmvBmsyc'
########################
#   SPOTIFY SETTINGS   #
########################

S_CLIENT_ID = '8418c11670bf4f88ae726dffed1eb90c'
S_CLIENT_SECRET = '2ca944e840764319888740d1ecd4e2d0'
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
