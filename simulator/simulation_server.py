from grid import get_grid
from Agent import Agent
import websockets
import asyncio
import json
import os

FPS = int(os.environ.get('FPS', 30))

g, mask = get_grid()

agents = [Agent(g) for _ in range(1000)]

sockets = set()


async def send_or_remove(socket, data):
    '''
    Sends data with websocket. Removes disconected websockets from set
    '''
    try:
        await socket.send(json.dumps(
            [agent.get_pos() for agent in agents])
        )
    except:
        sockets.remove(socket)


async def step_simulation():
    '''
    Do one simulation step and after finishing do next
    '''
    loop = asyncio.get_event_loop()

    for agent in agents:
        agent.step()

    for socket in sockets:
        loop.create_task(
            send_or_remove(socket, json.dumps(
                [agent.get_pos() for agent in agents])
            )
        )

    await asyncio.sleep(1/FPS)
    loop.create_task(step_simulation())


async def register_connection(websocket, path):
    '''
    register websocket connection
    '''
    sockets.add(websocket)
    await websocket.wait_closed()


start_server = websockets.serve(register_connection, "0.0.0.0", 8080)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_until_complete(step_simulation())
asyncio.get_event_loop().run_forever()
