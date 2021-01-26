from Simulator import Simulation, getTargetSize
from Agent import Agent
import websockets
import asyncio
import json
import os

FPS = int(os.environ.get('FPS', 30))
FRAMESKIP = int(os.environ.get('FRAMESKIP', 10))
WS_PORT = int(os.environ.get('WS_PORT', 8081))

sim = Simulation()

sockets = set()

size = getTargetSize()

async def send_or_remove(socket, data):
    '''
    Sends data with websocket. Removes disconected websockets from set
    '''
    try:
        await socket.send(
            json.dumps(data)
        )
    except:
        sockets.remove(socket)


async def step_simulation():
    '''
    Do one simulation step and after finishing do next
    '''
    loop = asyncio.get_event_loop()

    for _ in range(FRAMESKIP):
        sim.step()

    points = [agent.get_pos() for agent in sim.agents]

    data = {
        "passengers": [
            {
                "id": str(i),
                "x": int(x*size[0]),
                "y": int(y*size[1])
            } for i, (x, y) in enumerate(points)
        ],
        "flights": sim.get_flights(),
        "gates": sim.get_gates()
    }

    for socket in sockets:
        loop.create_task(
            send_or_remove(
                socket,
                data
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


start_server = websockets.serve(register_connection, "0.0.0.0", WS_PORT)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_until_complete(step_simulation())
asyncio.get_event_loop().run_forever()
