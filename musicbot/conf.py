"""Configurations functions."""

import importlib
import os
import tempfile

import spotipy.util

from . import settings


def reset_config():
    """Reset settings to default value."""
    save_config("CHANNEL_ID", '')
    save_config("DISCORD_TOKEN", '')
    save_config("S_CLIENT_ID", '')
    save_config("S_CLIENT_SECRET", '')


def reconfigure():
    """Reconfigure all necessary attributes on settings.py."""
    print("Please insert the following information: ")
    save_channel_id()
    save_discord_token()
    save_spotify_id()
    save_spotify_client_secret()
    importlib.reload(settings)


def save_channel_id():
    """Save channel id."""
    result = input("Channel ID of the bot:")
    save_config("CHANNEL_ID", result)


def save_discord_token():
    """Save Discord token."""
    result = input("Token Discord:")
    save_config("DISCORD_TOKEN", result)


def save_spotify_id():
    """Save Spotify id."""
    result = input("Spotify ID:")
    save_config("S_CLIENT_ID", result)


def save_spotify_client_secret():
    """Save Spotify client secret."""
    result = input("Spotify Client Secret:")
    save_config("S_CLIENT_SECRET", result)


def save_config(attribute, value):
    """Save an attribute value to the config file."""
    # temp file to copy settings.py
    tmp = tempfile.NamedTemporaryFile(mode="r+")

    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

    with open(os.path.join(__location__, "settings.py"), "r") as f:
        for line in f:
            if line[:len(attribute)] == attribute:
                tmp.write(attribute + " = " + "'" + value + "'\n")
            else:
                tmp.write(line)
    # rewind at the beginning of the tmp file
    tmp.seek(0)

    with open(os.path.join(__location__, "settings.py"), "w") as f:
        for line in tmp:
            f.write(line)


def config():
    """Configures the settings."""
    settings_dict = {
        'CHANNEL_ID': [settings.CHANNEL_ID, save_channel_id],
        'DISCORD_TOKEN': [settings.DISCORD_TOKEN, save_discord_token],
        'S_CLIENT_ID': [settings.S_CLIENT_ID, save_spotify_id],
        'S_CLIENT_SECRET': [settings.S_CLIENT_SECRET,
                            save_spotify_client_secret]
    }

    for key in settings_dict.values():
        if not key[0]:
            key[1]()
            importlib.reload(settings)

    settings.S_TOKEN = spotipy.util. \
        prompt_for_user_token('userSpotify',
                              scope=settings.S_SCOPE,
                              client_id=settings.S_CLIENT_ID,
                              client_secret=settings.S_CLIENT_SECRET,
                              redirect_uri=settings.S_REDIRECT_URI)
