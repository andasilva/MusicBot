"""Main program."""

import asyncio
import conf

from bot import startBot
from APIs import api_call


async def mainLoop(token):
    """Run main program."""
    response = await api_call(conf.DISCORD_URL + "/gateway", conf.DISCORD_HEADER)
    await startBot(response['url'], token)


def openSpotify():
    """Start a webdriver and go on Spotify wepage."""
    conf.driver.get("https://open.spotify.com/browse/featured")

    hasAccount = conf.driver.find_element_by_id('has-account')
    hasAccount.click()

    loginUsr = conf.driver.find_element_by_id('login-usr')
    loginUsr.clear()
    loginUsr.send_keys("SPOTIFY USERNAME") # Optional

    loginPass = conf.driver.find_element_by_id('login-pass')
    loginPass.clear()
    loginPass.send_keys("SPOTIFY PASSWORD") # Optional


if __name__ == "__main__":
    # Launch the program
    openSpotify()
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(mainLoop(conf.DISCORD_TOKEN))
    loop.close()
