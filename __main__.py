"""Main program."""

import asyncio
import conf

from bot import startBot
from apis import DiscordClient, SpotifyClient

async def mainLoop(discord_client, spotify_client):
    """Run main program."""
    response = await discord_client.api_call("/gateway")
    await startBot(response['url'], discord_client, spotify_client)


def openSpotify():
    """Start a webdriver and go on Spotify wepage."""

    conf.driver.get("https://open.spotify.com/browse/featured")

    hasAccount = conf.driver.find_element_by_id('has-account')
    hasAccount.click()

    loginUsr = conf.driver.find_element_by_id('login-usr')
    loginUsr.clear()
    loginUsr.send_keys("...") # Optional

    loginPass = conf.driver.find_element_by_id('login-pass')
    loginPass.clear()
    loginPass.send_keys("...") # Optional

if __name__ == "__main__":
    # Launch the program
    openSpotify()

    discord_client = DiscordClient(conf.DISCORD_TOKEN)
    spotify_client = SpotifyClient(conf.SPOTIFY_TOKEN)

    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(mainLoop(discord_client, spotify_client))
    loop.close()
