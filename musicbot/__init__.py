"""MusicBot bot package."""

import sys

import musicbot


if sys.version_info < (3, 5):
    raise ImportError("MusicBot requires Python 3.6+.")
