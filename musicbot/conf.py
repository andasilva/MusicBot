"""Configurations functions"""
import spotipy
import musicbot.settings
import tempfile
import spotipy.util


def reset_config():
    """Reset settings to default value"""
    save_config("CHANNEL_ID", '')
    save_config("DISCORD_TOKEN", '')
    save_config("S_CLIENT_ID", '')
    save_config("S_CLIENT_SECRET", '')


def reconfigure():
    """Reconfigure all necessary attributes on settings.py"""

    print("Please insert the following information: ")
    save_channel_id()
    save_discord_token()
    save_spotify_id()
    save_spotify_client_secret()


def save_channel_id():
    result = input("Channel ID of the bot:")
    save_config("CHANNEL_ID", result)


def save_discord_token():
    result = input("Token Discord:")
    save_config("DISCORD_TOKEN", result)


def save_spotify_id():
    result = input("Spotify ID:")
    save_config("S_CLIENT_ID", result)


def save_spotify_client_secret():
    result = input("Spotify Client Secret:")
    save_config("S_CLIENT_SECRET", result)


def save_config(attribute, value):
    """save an attribute value to the config file"""

    # temp file to copy settings.py
    tmp = tempfile.NamedTemporaryFile(mode="r+")

    with open("settings.py", "r") as f:
        for line in f:
            if line[:len(attribute)] == attribute:
                tmp.write(attribute + " = " + "'" + value + "'\n")
            else:
                tmp.write(line)
    # rewind at the beginning of the tmp file
    tmp.seek(0)

    with open("settings.py", "w") as f:
        for line in tmp:
            f.write(line)


def config():
    """Configures the settings"""

    musicbot.settings.CHANNEL_ID = musicbot.settings.CHANNEL_ID \
        if musicbot.settings.CHANNEL_ID != '' else save_channel_id()
    musicbot.settings.DISCORD_TOKEN = musicbot.settings.DISCORD_TOKEN \
        if musicbot.settings.DISCORD_TOKEN != '' else save_discord_token()
    musicbot.settings.S_CLIENT_ID = musicbot.settings.S_CLIENT_ID \
        if musicbot.settings.S_CLIENT_ID != '' else save_spotify_id()
    musicbot.settings.S_CLIENT_SECRET = musicbot.settings.S_CLIENT_SECRET \
        if musicbot.settings.S_CLIENT_SECRET != '' \
        else save_spotify_client_secret()

    musicbot.settings.S_TOKEN = spotipy.util.prompt_for_user_token('...',
                                                                   scope=musicbot.settings.S_SCOPE,
                                                                   client_id=musicbot.settings.S_CLIENT_ID,
                                                                   client_secret=musicbot.settings.S_CLIENT_SECRET,
                                                                   redirect_uri=musicbot.settings.S_REDIRECT_URI)
