"""Global configuration variables."""

import botFunctions
import spotipy.util as util


DISCORD_URL = "https://discordapp.com/api"
"""Discord HTTP API endpoint."""

DISCORD_TOKEN = ...

SPOTIFY_CLIENT_ID = ...

SPOTIFY_CLIENT_SECRET = ...

SPOTIFY_REDIRECT_URI = 'https://discordapp.com/channels/@me'

SPOTIFY_URL = f"https://accounts.spotify.com/authorize/?" \
              f"client_id={SPOTIFY_CLIENT_ID}&" \
              f"response_type=code&" \
              f"redirect_uri={SPOTIFY_REDIRECT_URI}&" \
              f"scope=user-read-birthdate%20user-read-private%20user-read-email%20user-read-currently-playing&" \
              f"state=34fFs29kd09"

def getSpotifyToken(scope):
    return util.prompt_for_user_token('Spotify Username', scope=scope,
                                           client_id=SPOTIFY_CLIENT_ID,
                                           client_secret=SPOTIFY_CLIENT_SECRET,
                                           redirect_uri=SPOTIFY_REDIRECT_URI)

commands = {'about_me': botFunctions.aboutMe,
            'currently_playing': botFunctions.currentlyPlaying,
            'genre': botFunctions.searchArtistGenre,
            'help': botFunctions.hlep}