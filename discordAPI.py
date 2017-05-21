"""Discord REST API tools."""

from aiohttp import ClientSession

from conf import DISCORD_URL


async def api_call(path, token, method="GET", **kwargs):
    """Do a request on the Discord's REST API."""
    default = {
        "headers": {
            "Authorization": f"Bot {token}",
            "User-Agent": "DiscordBot (http://he-arc.ch/, 0.1)"
        }
    }

    kwargs = dict(default, **kwargs)

    with ClientSession() as session:
        async with session.request(method, f"{DISCORD_URL}{path}", **kwargs) as response:
            if 200 == response.status:
                return await response.json()
            elif 204 == response.status:
                return {}
            else:
                body = await response.text()
                raise AssertionError(f"{response.status} {response.reason} was unexpected.\n{body}")