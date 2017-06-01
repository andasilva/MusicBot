"""API tools for Spotify and Discord."""

from aiohttp import ClientSession


class RestClient:
    """Base class REST client used for different apis."""

    def __init__(self, token):
        self.token = token

    async def api_call(self, url, method="GET", **kwargs):
        pass

    async def httpResponseStatus(self, response):
        """Common http responses."""
        if 200 == response.status:
            return await response.json()
        elif 204 == response.status:
            return {}

    @property
    def getToken(self):
        return self.token

class DiscordClient(RestClient):
    """Discord client for api calls."""

    def __init__(self, token):
        RestClient.__init__(self, token)
        self.endpoint = "https://discordapp.com/api"
        self.header = {
            "headers": {
                "Authorization": f"Bot {self.token}",
                "User-Agent": "DiscordBot (http://he-arc.ch/, 0.1)"
            }
        }

    async def api_call(self, url, method="GET", **kwargs):
        """Do a request on the Discord's REST API."""

        kwargs = dict(self.header, **kwargs)

        with ClientSession() as session:
            async with session.request(method, f"{self.endpoint}{url}", **kwargs) as response:
                if response.status in (200, 204):
                    return await RestClient.httpResponseStatus(self, response)
                else:
                    body = await response.text()
                    raise AssertionError(f"{response.status} {response.reason} was unexpected.\n{body}")


class SpotifyClient(RestClient):
    """Spotify client for api calls."""

    def __init__(self, token):
        RestClient.__init__(self, token)
        self.endpoint = "https://api.spotify.com/v1"
        self.header = {
            "headers": {
                "Authorization": f"Bearer {self.token}",
                "User-Agent": "DiscordBot (http://he-arc.ch/, 0.1)"
            }
        }

    async def api_call(self, url, method="GET", **kwargs):
        """Do a request on the Spotify's REST API."""

        kwargs = dict(self.header, **kwargs)

        with ClientSession() as session:
            async with session.request(method, f"{self.endpoint}{url}", **kwargs) as response:
                if response.status in (200, 204):
                    return await RestClient.httpResponseStatus(self, response)
                elif 403 == response.status:
                    return "You must have a premium Spotify account for this feature."
                elif 404 == response.status:
                    return "Error, device not found."
                else:
                    body = await response.text()
                    raise AssertionError(f"{response.status} {response.reason} was unexpected.\n{body}")