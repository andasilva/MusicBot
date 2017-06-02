"""API tools for Spotify and Discord."""

from aiohttp import ClientSession


class RestClient:
    """Base class REST client used for different apis."""

    def __init__(self, token):
        """Init rest client."""
        self._token = token

    async def api_call(self, url, method="GET", **kwargs):
        """Abstract api_call function."""
        raise NotImplementedError

    @property
    def token(self):
        """Token getter."""
        return self._token


class DiscordClient(RestClient):
    """Discord client for api calls."""

    def __init__(self, token):
        """Init discord client."""
        super().__init__(token)
        self.endpoint = "https://discordapp.com/api"
        self.header = {
            "headers": {
                "Authorization": f"Bot {self._token}",
                "User-Agent": "DiscordBot (http://he-arc.ch/, 0.1)"
            }
        }

    async def api_call(self, url, method="GET", **kwargs):
        """Do a request on the Discord's REST API."""
        kwargs = dict(self.header, **kwargs)

        with ClientSession() as session:
            async with session.request(
                    method,
                    f"{self.endpoint}{url}",
                    **kwargs
            ) as response:
                if response.status in (200, 204):
                    return await http_response_status(response)
                else:
                    body = await response.text()
                    raise UnexpectedHttpStatusError(
                        response.status,
                        response.reason, body
                    )


class SpotifyClient(RestClient):
    """Spotify client for api calls."""

    def __init__(self, token):
        """Init spotify client."""
        super().__init__(token)
        self.endpoint = "https://api.spotify.com/v1"
        self.header = {
            "headers": {
                "Authorization": f"Bearer {self._token}",
                "User-Agent": "DiscordBot (http://he-arc.ch/, 0.1)"
            }
        }

    async def api_call(self, url, method="GET", **kwargs):
        """Do a request on the Spotify's REST API."""
        kwargs = dict(self.header, **kwargs)

        with ClientSession() as session:
            async with session.request(
                    method,
                    f"{self.endpoint}{url}",
                    **kwargs) as response:
                if response.status in (200, 204):
                    return await http_response_status(response)
                elif 403 == response.status:
                    return "You must have a premium Spotify " \
                           "account for this feature."
                elif 404 == response.status:
                    return "Error, device not found."
                else:
                    body = await response.text()
                    raise UnexpectedHttpStatusError(
                        response.status,
                        response.reason, body
                    )


class UnexpectedHttpStatusError(Exception):
    """Exception raise for unexpected HTTP status response."""

    def __init__(self, status, reason, body):
        """Init unexpected http status errors."""
        self.status = status
        self.reason = reason
        self.body = body


async def http_response_status(response):
    """Handle common HTTP responses."""
    if 200 == response.status:
        return await response.json()
    elif 204 == response.status:
        return {}
