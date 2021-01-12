from grid import Grid
import random
import numpy as np
from scipy.spatial import distance_matrix
import pickle
import os
from math import sqrt, exp
import json
from datetime import datetime, timedelta


class Agent:
    def __init__(self, grid, pos=None) -> None:
        self.target = None
        self.path = None
        self.speed = 0.75
        self.grid = grid
        self.pos = pos
        self.velocity = np.zeros(2)
        self.in_bounds = True
        self.grid_pos = pos

    def preferred_velocity(self):
        def normalize(v):
            norm = np.linalg.norm(v)
            if norm == 0:
                return v
            return v / norm

        while self.target is None:
            self.target = random.choice(self.grid.goals)
            self.path = self.grid.paths[tuple(self.target)]

        grid_pos, self.in_bounds = self.grid.pos_to_grid(tuple(self.pos))
        # if not in_bounds:
        #     self.pos = grid_pos
        next_pos = self.path[tuple(grid_pos)]
        vec = normalize(
            np.array([next_pos[0]-grid_pos[0], next_pos[1]-grid_pos[1]]))*self.speed

        if (grid_pos[0]-self.target[0])**2 + (grid_pos[1]-self.target[1])**2 < 25:
            self.target = None

        return vec

    def get_pos(self):
        return (self.pos[0]/self.grid.grid_size[0], self.pos[1]/self.grid.grid_size[1])


airports = [
    'Suceava', 'Reykjavik', 'Tel', 'Poznan', 'Tirana', 'Frankfurt', 'Cluj-Napoca', 'Debrecen', 'Wroclaw', 'Milan', 'Iasi', 'Sofia', 'Dublin', 'Belfast', 'Tenerife', 'Faro', 'Bacau', 'Krakow', 'Kaunas', 'Budapest', 'Constanta', 'Marrakesh', 'Lublin', 'Kiev', 'Timisoara', 'Vilnius', 'Lisbon', 'Katowice', 'Poprad', 'Gdansk', 'Malaga', 'Warsaw', 'Luqa', 'Palma', 'Istanbul', 'Bucharest', 'Olsztyn', 'St.', 'Larnaca',
    'Craiova', 'Vienna', 'Athens', 'Moscow', 'Chisinau', 'Thessaloniki', 'Targu', 'Bratislava', 'Belgrade', 'Riga', 'Varna', 'Kosice'
]


class Flights:
    def __init__(self, length):
        self.flights_per_day = 100
        number_of_flights = int(self.flights_per_day * length)

        length = length*24*60

        self.arrivals = [
            {
                "id": i,
                "scheduled": random.uniform(15, length),
                "from": random.choice(airports),
                "to": "Luton",
                "delay": 0,
                "gate": -1
            }
            for i in range(number_of_flights)
        ]

        self.departures = [
            {
                "id": i,
                "scheduled": random.uniform(15, length),
                "to": random.choice(airports),
                "from": "Luton",
                "delay": 0,
                "gate": -1
            }
            for i in range(number_of_flights)
        ]

        # self.flights.sort(key=lambda x: x["scheduled"])

    def update(self, time):
        # remove flights 15 minutes after arrival
        self.arrivals = list(
            filter(
                lambda x: x["scheduled"] + x["delay"] +
                15 > time, self.arrivals
            )
        )
        # remove flights after departure
        self.departures = list(
            filter(
                lambda x: x["scheduled"] + x["delay"] > time, self.departures
            )
        )

        # TODO: update delays


class Simulation:
    def __init__(self):
        size = 500
        if os.path.isfile('cache/grid.pickle'):
            with open('cache/grid.pickle', 'rb') as f:
                self.grid = pickle.loads(f.read())
        else:
            self.grid = Grid()
            with open('cache/grid.pickle', 'wb') as f:
                f.write(pickle.dumps(self.grid))

        self.mask = self.grid.mask
        self.agents = [Agent(self.grid, pos=self.grid.random())
                       for _ in range(size)]

        self.flights = Flights(1)

        self.agent_radius = 1
        self.agent_mass = 1
        self.alpha = 0.1  # social scaling constant
        self.beta = 10  # agents personal space drop-off constant
        self.tau = 1  # reaction time

        self.time = 0
        self.time_step = 1/120

    def get_flights(self):
        arrivals = self.flights.arrivals
        departures = self.flights.departures
        flights = (arrivals + departures)
        flights.sort(key=lambda x: x["scheduled"] + x["delay"])

        return [
            {
                "id": str(flight['id']),
                "flightNum": f"W{flight['id']}",
                "from": flight['from'],
                "dest": flight['to'],
                "status": "Delayed" if flight['delay'] != 0 else "On Time",
                "departure": (datetime(2021, 1, 12) + timedelta(minutes=flight["scheduled"]+flight["delay"])).isoformat(),
                "gateNum": "0",
            }
            for flight in flights
        ]

    def step(self):
        self.time += self.time_step
        self.flights.update(self.time)

        positions = np.array([a.pos for a in self.agents])
        preffered_velocities = np.array(
            [a.preferred_velocity() for a in self.agents])
        velocities = np.array([a.velocity for a in self.agents])
        # distances = distance_matrix(positions, positions)[..., np.newaxis]
        # normals = np.empty((len(self.agents), len(self.agents), 2))
        # for i in range(normals.shape[0]):
        #     for j in range(normals.shape[1]):
        #         normals[i, j] = (positions[i]-positions[j])[::-1]
        # social_forces = self.alpha * \
        #     np.exp((2*self.agent_radius-distances)/self.beta)*normals

        # np.fill_diagonal(social_forces[:, :, 0], 0)
        # np.fill_diagonal(social_forces[:, :, 1], 0)

        # social_forces = social_forces.sum(axis=1)
        attraction_forces = self.agent_mass * \
            (preffered_velocities - velocities)/self.tau

        forces = attraction_forces  # + social_forces
        for i, agent in enumerate(self.agents):
            # obstacle_force = np.zeros(2)
            # obstacles_radius = 10
            # for x in range(-obstacles_radius, obstacles_radius+1):
            #     for y in range(-obstacles_radius, obstacles_radius+1):
            #         pos = (agent.grid_pos[0]+x, agent.grid_pos[1]+y)
            #         if self.mask[pos]==0:
            #             obstacle_force += 1 * exp((self.agent_radius-sqrt(x**2+y**2))/1) * np.array([-x, -y])

            agent.velocity += forces[i]  # + obstacle_force

            # agent.velocity = preffered_velocities[i]
            agent.pos = np.array(agent.pos) + agent.velocity


def getTargetSize():
    with open('layout.json') as f:
        data = json.loads(f.read())
    return data['image-size']


if __name__ == '__main__':
    sim = Simulation()
    sim.step()