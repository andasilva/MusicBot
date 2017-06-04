"""Music bot which can communicate with YouTube."""

import asyncio
import json
import zlib

import aiohttp

from . import bot_functions, settings

API_VERSION = 6

# https://discordapp.com/developers/docs/topics/gateway#gateway-op-codes
DISPATCH = 0
HEARTBEAT = 1
IDENTIFY = 2
HELLO = 10
HEARTBEAT_ACK = 11


async def send_message(recipient_id, content, discord_client):
    """Send a message to the given user."""
    channel = await discord_client.api_call(
        "/users/@me/channels",
        "POST",
        json={"recipient_id": recipient_id}
    )

    return await discord_client.api_call(
        f"/channels/{channel['id']}/messages",
        "POST",
        json={"content": content}
    )


last_sequence = None


async def heartbeat(web_socket, interval):
    """Keep alive the connexion with Discord."""
    while True:
        await asyncio.sleep(interval / 1000)
        print("> Heartbeat")
        await web_socket.send_json(
            {'op': HEARTBEAT,
             'd': last_sequence}
        )


async def identify(web_socket, token):
    """Identifie the bot with the Web Socket (essential)."""
    await web_socket.send_json({
        'op': IDENTIFY,
        'd': {
            'token': token,
            'properties': {},
            'compress': True,
            'large_threshold': 250
        }
    })


async def start_bot(web_socket, discord_client, spotify_client):
    """Start the bot with the given Web Socket address."""
    global last_sequence  # global is necessary in order to modify the variable
    with aiohttp.ClientSession() as session:
        async with session.ws_connect(
                f"{web_socket}?v=6&encoding=json") as web_socket:
            async for msg in web_socket:
                if msg.tp == aiohttp.WSMsgType.TEXT:
                    data = json.loads(msg.data)
                elif msg.tp == aiohttp.WSMsgType.BINARY:
                    data = json.loads(zlib.decompress(msg.data))
                else:
                    print("?", msg.tp)

                if data['op'] == HELLO:
                    asyncio.ensure_future(
                        heartbeat(
                            web_socket,
                            data['d']['heartbeat_interval']
                        )
                    )
                    await identify(web_socket, discord_client.token)

                elif data['op'] == HEARTBEAT_ACK:
                    print("< Heartbeat ACK")

                elif data['op'] == DISPATCH:
                    last_sequence = data['s']

                    # Make sure we're in the right channel
                    if (data['t'] == "MESSAGE_CREATE" and
                       data['d']['channel_id'] == settings.CHANNEL_ID):

                        data_partition = data['d']['content'].partition(' ')

                        # Make sure the command exist
                        if dir(bot_functions).__contains__(
                                data_partition[0]):

                            content = await getattr(
                                bot_functions,
                                data_partition[0]
                            )(spotify_client, data_partition[2])

                            # Send the retrieved data to
                            # the user, not to the bot.
                            await send_data(content, data, discord_client)

                        else:  # shows the user how to access help
                            content = """Sorry, I don't know this command.
                                         You can try 'help' for
                                         more informations."""

                            await send_data(content, data, discord_client)
                    else:
                        print('Todo?', data['t'])
                else:
                    print("Unknown?", data)


async def send_data(content, data, discord_client):
    """Send the retrieved data to the user, not to the bot."""
    if data['d']['author']['username'] != 'music-bot':
        asyncio.ensure_future(
            send_message(
                data['d']['author']['id'],
                content,
                discord_client
            )
        )
