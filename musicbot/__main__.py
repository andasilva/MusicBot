"""Main program."""

import asyncio
import sys

from . import settings
from .apis import DiscordClient, SpotifyClient
from .bot import start_bot
from .conf import config, reconfigure


async def main_loop(discord_client, spotify_client):
    """Run main program."""
    response = await discord_client.api_call("/gateway")
    await start_bot(response['url'], discord_client, spotify_client)


if __name__ == "__main__":
    # Launch the program
    if len(sys.argv) > 1 and sys.argv[1] == 'reset':
        # Reconfigure settings of the applications
        reconfigure()
    else:
        # Check if settings are configured (perform a configuration if needed)
        config()

    discord_client = DiscordClient(settings.DISCORD_TOKEN)
    spotify_client = SpotifyClient(settings.S_TOKEN)

    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(main_loop(discord_client, spotify_client))
    loop.close()
