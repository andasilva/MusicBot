"""Music bot which can communicate with YouTube"""

import aiohttp
import asyncio
import bot_functions
import conf
import json
import zlib


API_VERSION = 6

# https://discordapp.com/developers/docs/topics/gateway#gateway-op-codes
DISPATCH = 0
HEARTBEAT = 1
IDENTIFY = 2
HELLO = 10
HEARTBEAT_ACK = 11


async def send_message(recipient_id, content, discord_client):
    """Send a message to the given user."""
    channel = await discord_client.api_call("/users/@me/channels", "POST", json={"recipient_id": recipient_id})
    return await discord_client.api_call(f"/channels/{channel['id']}/messages", "POST", json={"content": content})


last_sequence = None


async def heartbeat(webSocket, interval):
    """Keep alive the connexion with Discord."""
    while True:
        await asyncio.sleep(interval / 1000)
        print("> Heartbeat")
        await webSocket.send_json({'op': HEARTBEAT,
                            'd': last_sequence})


async def identify(webSocket, token):
    """Identifie the bot with the Web Socket (essential)."""
    await webSocket.send_json({'op': IDENTIFY,
                        'd': {'token': token,
                              'properties': {},
                              'compress': True,  # imply the code snippet linked to zlib, not necessary.
                              'large_threshold': 250}})


async def startBot(webSocket, discord_client, spotify_client):
    """Start the bot with the given Web Socket address."""
    global last_sequence  # global is necessary in order to modify the variable
    with aiohttp.ClientSession() as session:
        async with session.ws_connect(f"{webSocket}?v=6&encoding=json") as webSocket:
            async for msg in webSocket:
                if msg.tp == aiohttp.WSMsgType.TEXT:
                    data = json.loads(msg.data)
                elif msg.tp == aiohttp.WSMsgType.BINARY:
                    data = json.loads(zlib.decompress(msg.data))
                else:
                    print("?", msg.tp)

                if data['op'] == HELLO:
                    asyncio.ensure_future(heartbeat(webSocket, data['d']['heartbeat_interval']))
                    await identify(webSocket, discord_client.token)

                elif data['op'] == HEARTBEAT_ACK:
                    print("< Heartbeat ACK")

                elif data['op'] == DISPATCH:
                    last_sequence = data['s']
                    if data['t'] == "MESSAGE_CREATE" and data['d']['channel_id'] == conf.CHANNEL_ID: # Make sure we're in the right channel
                        if dir(bot_functions).__contains__(data['d']['content'].partition(' ')[0]): # Make sure the command exist
                            try:
                                content = await getattr(bot_functions, data['d']['content'].partition(' ')[0])(spotify_client) # Command without arg
                            except:
                                content = await getattr(bot_functions, data['d']['content'].partition(' ')[0])(data['d']['content'].partition(' ')[2], spotify_client) # Command with arg
                            if data['d']['author']['username'] != 'music-bot' and content != {}: # Send the retrieved data to the user, not to the bot
                                asyncio.ensure_future(send_message(data['d']['author']['id'], content, discord_client))
                        else: # shows the user how to access help
                            content = "Sorry, I don't know this command. You can try 'help' for more informations."
                            if data['d']['author']['username'] != 'music-bot': # Send the retrieved data to the user, not to the bot
                                asyncio.ensure_future(send_message(data['d']['author']['id'], content, discord_client))
                    else:
                        print('Todo?', data['t'])
                else:
                    print("Unknown?", data)