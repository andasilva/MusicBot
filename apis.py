"""API tools for Spotify and Discord."""

from aiohttp import ClientSession


async def api_call(url, header, method="GET", **kwargs):
    """Do a request on the Discord's/Spotify's REST API."""

    kwargs = dict(header, **kwargs)

    with ClientSession() as session:
        async with session.request(method, f"{url}", **kwargs) as response:
            if 200 == response.status:
                return await response.json()
            elif 204 == response.status:
                return {}
            elif 403 == response.status:
                return "You must have a premium Spotify account for this feature."
            elif 404 == response.status:
                return "Error, device not found."
            else:
                body = await response.text()
                raise AssertionError(f"{response.status} {response.reason} was unexpected.\n{body}")