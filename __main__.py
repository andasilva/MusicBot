"""Main program."""

import os
import sys
import asyncio

from discordAPI import  api_call
from bot import  startBot
from conf import DISCORD_TOKEN

async def main(token):
    """Run main program."""
    response = await api_call("/gateway", token)
    await startBot(response['url'], token)


if __name__ == "__main__":
    # Launch the program
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(main(DISCORD_TOKEN))
    loop.close()
