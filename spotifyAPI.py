"""Spotify REST API tools."""

from aiohttp import ClientSession


async  def api_call(url, token, method="GET", **kwargs):
    """Do a request on the Spotify's REST API."""
    default = {
        "headers": {
            "Authorization": f"Bearer {token}",
            "User-Agent": "DiscordBot (http://he-arc.ch/, 0.1)"
        }
    }

    kwargs = dict(default, **kwargs)

    with ClientSession() as session:
        async with session.request(method, f"{url}", **kwargs) as response:
            if 200 == response.status:
                return await response.json()
            elif 202 == response.status:
                return "Wait 5 seconds and retry."
            elif 204 == response.status:
                return {}
            elif 403 == response.status:
                return "You must have a premium Spotify account for this feature."
            elif 404 == response.status:
                return "Error, device not found."
            else:
                body = await response.text()
                raise AssertionError(f"{response.status} {response.reason} was unexpected.\n{body}")