# Airport simulator for evaluating airport gate assignment problem. Part of ariportAI project.

## Prerequisites
Python 3 is required to run this application. Cuda toolkit must be installed. If you are using Conda type:
```
$ conda install cudatoolkit
```
Refer to [numba requirements](https://numba.readthedocs.io/en/stable/cuda/overview.html#requirements).


## Installation
Installing from git:

```
$ git clone https://github.com/burnpiro/airport-ai.git
$ cd airport-ai/simulator
$ pip install .
```

Installing from pypi:
```
$ pip install airportAI-simulator
```

## Usage
Import `Simulator` module and create `Simulation` object.

```python
from Simulator import Simulation
sim = Simulation()

# stepping simulation
sim.step()

# get agents and theier properties
agents = sim.agents
pos = agents[0].get_pos()

# get flight schedule
flights = sim.get_flights()

# get gates status
gates = sim.get_gates()
```

