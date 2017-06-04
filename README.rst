========
MusicBot
========

.. image:: https://travis-ci.org/andasilva/MusicBot.svg?branch=master
   :target: https://travis-ci.org/andasilva/MusicBot
   :alt: Build Status

Discord bot made with Python which is aimed to control Spotify.

Getting started
================

Explanations for setting up and running the bot.

Requirements
------------

- `Python 3.6 <https://www.python.org/>`_
- `aiohttp 2.1.0 <https://pypi.python.org/pypi/aiohttp>`_
- `Selenium-Python <https://selenium-python.readthedocs.io/>`_
- `Spotipy <https://spotipy.readthedocs.io/en/latest/>`_

Installation
------------

TODO...

Configuration
-------------

At the first start of the bot, some configurations questions
are asked to the user from command line. These are the following:

- Channel ID of the bot
- Discord token
- Spotify token
- Spotify Client ID/Secret

Once they're configured, there's no need to configure them again.

webdriver
---------

The bot may use a chrome webdriver in order to manage the Spotify app by itself.
The driver can be found here: `Chrome webdriver <https://sites.google.com/a/chromium.org/chromedriver/downloads>`_

Note that the driver must be in the user's PATH.

Bibliography
============

- `A Discord bot with asyncio <https://tutorials.botsfloor.com/a-discord-bot-with-asyncio-359a2c99e256>`_
- `Discord API Reference <https://discordapp.com/developers/docs/reference>`_
- `Spotify API Reference <https://developer.spotify.com/web-api>`_
- `Travisbos <https://github.com/greut/travisbot>`_
