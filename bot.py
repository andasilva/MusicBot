"""Music bot which can communicate with YouTube"""

import asyncio
import json
import zlib
import APIs
import aiohttp
import conf

API_VERSION = 6

# https://discordapp.com/developers/docs/topics/gateway#gateway-op-codes
DISPATCH = 0
HEARTBEAT = 1
IDENTIFY = 2
HELLO = 10
HEARTBEAT_ACK = 11


async def send_message(recipient_id, content, token):
    """Send a message to the given user."""
    channel = await APIs.api_call(conf.DISCORD_URL + "/users/@me/channels", conf.DISCORD_HEADER, "POST", json={"recipient_id": recipient_id})
    return await APIs.api_call(conf.DISCORD_URL + f"/channels/{channel['id']}/messages", conf.DISCORD_HEADER, "POST", json={"content": content})


last_sequence = None


async def heartbeat(ws, interval):
    """Keep alive the connexion with Discord."""
    while True:
        await asyncio.sleep(interval / 1000)
        print("> Heartbeat")
        await ws.send_json({'op': HEARTBEAT,
                            'd': last_sequence})


async def identify(ws, token):
    """Identifie the bot with the Web Socket (essential)."""
    await ws.send_json({'op': IDENTIFY,
                        'd': {'token': token,
                              'properties': {},
                              'compress': True,  # imply the code snippet linked to zlib, not necessary.
                              'large_threshold': 250}})


async def startBot(ws, token):
    """Start the bot with the given Web Socket address."""
    global last_sequence  # global is necessary in order to modify the variable
    with aiohttp.ClientSession() as session:
        async with session.ws_connect(f"{ws}?v=6&encoding=json") as ws:
            async for msg in ws:
                if msg.tp == aiohttp.WSMsgType.TEXT:
                    data = json.loads(msg.data)
                elif msg.tp == aiohttp.WSMsgType.BINARY:
                    data = json.loads(zlib.decompress(msg.data))
                else:
                    print("?", msg.tp)

                if data['op'] == HELLO:
                    asyncio.ensure_future(heartbeat(ws, data['d']['heartbeat_interval']))
                    await identify(ws, token)

                elif data['op'] == HEARTBEAT_ACK:
                    print("< Heartbeat ACK")

                elif data['op'] == DISPATCH:
                    last_sequence = data['s']
                    if data['t'] == "MESSAGE_CREATE":
                        if conf.commands.__contains__(data['d']['content'].partition(' ')[0]): # Make sure the command exist
                            try:
                                content = await conf.commands[data['d']['content'].partition(' ')[0]]()  # Command without arg
                            except:
                                content = await conf.commands[data['d']['content'].partition(' ')[0]](data['d']['content'].partition(' ')[2]) # Command with arg

                            if data['d']['author']['username'] != 'music-bot' and content != {}: # Send the retrieved data to the user, not to the bot
                                asyncio.ensure_future(send_message(data['d']['author']['id'], content, token))
                        else: # shows the user how to access help
                            content = "Sorry, I don't know this command. You can try 'help' for more informations."
                            if data['d']['author']['username'] != 'music-bot': # Send the retrieved data to the user, not to the bot
                                asyncio.ensure_future(send_message(data['d']['author']['id'], content, token))
                    else:
                        print('Todo?', data['t'])
                else:
                    print("Unknown?", data)