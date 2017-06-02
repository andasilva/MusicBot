"""Main program."""

import asyncio

from musicbot.apis import DiscordClient, SpotifyClient
from musicbot.bot import start_bot
import musicbot.conf as conf


async def mainLoop(discord_client, spotify_client):
    """Run main program."""
    response = await discord_client.api_call("/gateway")
    await start_bot(response['url'], discord_client, spotify_client)

if __name__ == "__main__":
    # Launch the program
    discord_client = DiscordClient(conf.DISCORD_TOKEN)
    spotify_client = SpotifyClient(conf.S_TOKEN)

    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(mainLoop(discord_client, spotify_client))
    loop.close()
