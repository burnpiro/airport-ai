from datetime import time
from Simulator import Simulation, getTargetSize
import json
import os
from tqdm import tqdm

FPS = int(os.environ.get('FPS', 2))
FRAMESKIP = int(os.environ.get('FRAMESKIP', 30))

sim = Simulation()

sockets = set()

size = getTargetSize()



def run_simulation(length=500):
    timestamps = []
    for i in tqdm(range(length)):        
        for _ in range(FRAMESKIP):
            sim.step()

        points = [agent.get_pos() for agent in sim.agents]
        ids = [agent.id for agent in sim.agents]

        data = {
            "passengers": [
                {
                    "id": str(id),
                    "x": int(x*size[0]),
                    "y": int(y*size[1])
                } for (x, y), id in zip(points, ids)
            ],
            "flights": sim.get_flights(),
            "gates": sim.get_gates()
        }

        timestamps.append({'timestamp': i ,**data})
    
    return timestamps


timestamps = run_simulation()[100:]

with open('out.json', 'w') as f:
    f.write(json.dumps(timestamps))