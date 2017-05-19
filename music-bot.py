"""Music bot which can communicate with YouTube"""

import asyncio
import json
import zlib

import aiohttp

TOKEN = 'MzEyMTcwNjk2MTQ5MTcyMjI1.C_79Dg.sNdHiMqcsPkVZ3c83uxwmvBmsyc'

URL = "https://discordapp.com/api"
HEADERS = {
    "Authorization": f"Bot {TOKEN}",
    "User-Agent": "DiscordBot (http://he-arc.ch/, 0.1)"
}

async def api_call(path, method="GET", **kwargs):
    """Do a request on the Discord's REST API."""
    default = {"headers": HEADERS}
    kwargs = dict(default, **kwargs)
    with aiohttp.ClientSession() as session:
        async with session.request(method, f"{URL}{path}", **kwargs) as response:
            if 200 == response.status:
                return await response.json()
            elif 204 == response.status:
                return {}
            else:
                body = await response.text()
                raise AssertionError(f"{response.status} {response.reason} was unexpected.\n{body}")

async def send_message(recipient_id, content):
    """Send a message to the given user."""
    channel = await api_call("/users/@me/channels", "POST", json={"recipient_id": recipient_id})
    return await api_call(f"/channels/{channel['id']}/messages", "POST", json={"content": content})

last_sequence = None

async def heartbeat(ws, interval):
    """Keep alive the connexion with Discord."""
    while True:
        await asyncio.sleep(interval / 1000)
        print("> Heartbeat")
        await ws.send_json({'op': 1,  # Heartbeat
                            'd': last_sequence})


async def identify(ws):
    """Identifie the bot with the Web Socket (essential)."""
    await ws.send_json({'op': 2,  # Identify
                        'd': {'token': TOKEN,
                              'properties': {},
                              'compress': True,  # imply the code snippet linked to zlib, not necessary.
                              'large_threshold': 250}})
        
async def start(ws):
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

                # https://discordapp.com/developers/docs/topics/gateway#gateway-op-codes
                if data['op'] == 10:  # Hello
                    asyncio.ensure_future(heartbeat(ws, data['d']['heartbeat_interval']))
                    await identify(ws)
                elif data['op'] == 11:  # Heartbeat ACK
                    print("< Heartbeat ACK")
                elif data['op'] == 0:  # Dispatch
                    last_sequence = data['s']
                    if data['t'] == "MESSAGE_CREATE":
                        print(data['d'])
                        if data['d']['author']['username'] in ['Quentin Vaucher', 'André Neto da Silva']:
                            task = asyncio.ensure_future(send_message(data['d']['author']['id'],
                                                                      data['d']['content']))
                            
                            if data['d']['content'] == 'quit':
                                print('Bye bye!')
                                # Wait for the message to be sent
                                await asyncio.wait([task])
                                break
                    else:
                        print('Todo?', data['t'])
                else:
                    print("Unknown?", data)


async def main():
    response = await api_call('/gateway')
    await start(response['url'])

    
# Launch the program 
loop = asyncio.get_event_loop()
loop.set_debug(True)
loop.run_until_complete(main())
loop.close()
