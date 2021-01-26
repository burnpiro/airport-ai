from .grid import Grid
import random
import numpy as np
from scipy.spatial import distance_matrix
import pickle
import os
from math import sqrt, exp, ceil
import json
from datetime import datetime, timedelta
from numba import cuda
from .flights import Flights
from .agent import Agent


class Simulation:
    def __init__(self):
        size = 1000
        if os.path.isfile('cache/grid.pickle'):
            with open('cache/grid.pickle', 'rb') as f:
                self.grid = pickle.loads(f.read())
        else:
            self.grid = Grid()
            with open('cache/grid.pickle', 'wb') as f:
                f.write(pickle.dumps(self.grid))

        self.mask = self.grid.mask
        # self.agents = [Agent(self.grid, pos=self.grid.random())
        #                for _ in range(size)]

        self.agents = []

        self.flights = Flights(1, gate_ids=list(self.grid.gates.keys()))

        self.agent_radius = 1
        self.agent_mass = 0.1
        self.alpha = 0.003  # social scaling constant
        self.beta = 5  # agents personal space drop-off constant
        self.tau = 0.1  # reaction time

        self.time = 0
        self.time_step = 1/60

    def get_flights(self):
        # arrivals = self.flights.arrivals
        # departures = self.flights.departures
        flights = [{'id': id, **flight}
                   for id, flight in self.flights.flights.items()]
        flights.sort(key=lambda x: x["scheduled"] + x["delay"])

        return [
            {
                "id": str(flight['id']),
                "flightNum": f"W{flight['id']}",
                "from": flight['from'],
                "dest": flight['to'],
                "status": "Delayed" if flight['delay'] != 0 else "On Time",
                "departure": (datetime(2021, 1, 12) + timedelta(minutes=flight["scheduled"]+flight["delay"])).isoformat(),
                "gateNum": flight['gate'],
            }
            for flight in flights
        ]

    def get_gates(self):
        return [
            {
                "gateId": gate_id,
                "flightId": flight_id
            }
            for gate_id, flight_id in self.flights.gates.items()
        ]

    @staticmethod
    @cuda.jit
    def make_simulation_step(positions, velocities, preferred_velocities, alpha, beta, tau, mass, radius, distances_buf, normals_buf, out):
        idx = cuda.grid(1)
        n = positions.shape[0]
        if idx >= n:
            return

        for i in range(n):
            positions[i, 0] = positions[i, 0] - positions[idx, 0]
            positions[i, 1] = positions[i, 1] - positions[idx, 1]

        for i in range(n):
            # distances_buf[i] = np.linalg.norm(positions[i])
            distances_buf[i] = sqrt(positions[i, 0]**2 + positions[i, 1]**2)
        # distances = np.linalg.norm(positions - positions[idx], axis=0)
        for i in range(n):
            normals_buf[i, 0] = -positions[i, 0]
            normals_buf[i, 1] = positions[i, 1]
            # normals_buf[i, 0] *= -1

        social_forces = normals_buf  # reuse buffer

        for i in range(n):
            force = alpha * exp((2*radius-distances_buf[i])/beta)
            social_forces[i, 0] = force*normals_buf[i, 0]
            social_forces[i, 1] = force*normals_buf[i, 1]

        social_forces[idx] = 0
        social_force_x = 0
        for i in range(n):
            social_force_x += social_forces[i, 0]

        if social_force_x > 10:
            social_force_x = 10

        social_force_y = 0
        for i in range(n):
            social_force_y += social_forces[i, 1]

        if social_force_y > 10:
            social_force_y = 10

        attraction_force_x = mass * \
            (preferred_velocities[idx, 0] - velocities[idx, 0])/tau

        attraction_force_y = mass * \
            (preferred_velocities[idx, 1] - velocities[idx, 1])/tau

        out[idx, 0] = attraction_force_x + social_force_x
        out[idx, 1] = attraction_force_y + social_force_y

    def step(self):
        self.time += self.time_step
        agents_to_spawn = self.flights.update(self.time, self.time_step)

        for agent in agents_to_spawn:
            pos = None
            dest = None
            to_flight = None

            if agent['position'] == 'entrance':
                pos = self.grid.entrance
            else:
                gate = agent['position']
                pos = self.grid.gates[gate]

            if agent['destination'] == 'exit':
                dest = 'exit'
            else:
                to_flight = self.flights.flights[agent['destination']]['id']
                dest = self.flights.flights[agent['destination']]['gate']
                # dest = self.grid.gates[gate]

            self.agents.append(
                Agent(self.grid, pos, dest, to_flight=to_flight))

        if len(self.agents) == 0:
            return

        # print(len(self.agents))

        positions = np.array([a.pos for a in self.agents], dtype=np.float64)
        preffered_velocities = np.array(
            [a.preferred_velocity() for a in self.agents])
        velocities = np.array([a.velocity for a in self.agents])

        forces = np.empty((positions.shape[0], 2))
        threadsperblock = 32
        self.make_simulation_step[ceil(velocities.size/threadsperblock), threadsperblock](
            positions,
            velocities,
            preffered_velocities,
            self.alpha,
            self.beta,
            self.tau,
            self.agent_mass,
            self.agent_radius,
            cuda.device_array(positions.shape[0]),  # distances buffer
            cuda.device_array_like(positions),  # normals buffer
            forces
        )
        # print(forces)
        # forces = Simulation.make_simulation_step(
        #     positions,
        #     velocities,
        #     preffered_velocities,
        #     self.alpha,
        #     self.beta,
        #     self.tau,
        #     self.agent_mass,
        #     self.agent_radius
        # )

        agents_to_remove = []
        for i, agent in enumerate(self.agents):
            direction = self.grid.direction_torwards_grid(self.grid.grid_pos(agent.pos))
            force = forces[i] + direction*10
            agent.velocity += (force/self.agent_mass) * \
                self.time_step  # + obstacle_force
            # agent.velocity = preffered_velocities[i]
            agent.pos = np.array(agent.pos) + agent.velocity*self.time_step

            if agent.reached_goal():
                if agent.goal_name == 'exit':
                    agents_to_remove.append(agent)
                else:
                    gate = self.flights.flights[agent.to_flight]['gate']
                    if self.flights.gates[gate] == gate:
                        agents_to_remove.append(agent)
                        self.flights.board_passenger(agent.goal_name)
                        print('agent reached gate')

        for agent in agents_to_remove:
            self.agents.remove(agent)

            # gridPos, in_bounds = self.grid.pos_to_grid(agent.pos)
            # if not in_bounds:
            #     agent.pos = gridPos

    def step2(self):
        self.time += self.time_step
        self.flights.update(self.time)

        positions = np.array([a.pos for a in self.agents])
        preffered_velocities = np.array(
            [a.preferred_velocity() for a in self.agents])
        velocities = np.array([a.velocity for a in self.agents])

        distances = distance_matrix(positions, positions)[..., np.newaxis]
        normals = np.empty((len(self.agents), len(self.agents), 2))
        for i in range(normals.shape[0]):
            for j in range(normals.shape[1]):
                normals[i, j] = (positions[i]-positions[j])[::-1]
        social_forces = self.alpha * \
            np.exp((2*self.agent_radius-distances)/self.beta)*normals

        np.fill_diagonal(social_forces[:, :, 0], 0)
        np.fill_diagonal(social_forces[:, :, 1], 0)

        social_forces = social_forces.sum(axis=1)

        attraction_forces = self.agent_mass * \
            (preffered_velocities - velocities)/self.tau

        forces = attraction_forces + social_forces
        for i, agent in enumerate(self.agents):
            # obstacle_force = np.zeros(2)
            # obstacles_radius = 10
            # for x in range(-obstacles_radius, obstacles_radius+1):
            #     for y in range(-obstacles_radius, obstacles_radius+1):
            #         pos = (agent.grid_pos[0]+x, agent.grid_pos[1]+y)
            #         if self.mask[pos]==0:
            #             obstacle_force += 1 * exp((self.agent_radius-sqrt(x**2+y**2))/1) * np.array([-x, -y])

            direction = self.grid.direction_torwards_grid(agent.grid_pos)
            force = forces[i] + direction*10

            agent.velocity += force  # + obstacle_force

            # agent.velocity = preffered_velocities[i]
            agent.pos = np.array(agent.pos) + agent.velocity
            gridPos, in_bounds = self.grid.pos_to_grid(agent.pos)
            if not in_bounds:
                agent.pos = gridPos


def getTargetSize():
    with open('layout.json') as f:
        data = json.loads(f.read())
    return data['image-size']


if __name__ == '__main__':
    sim = Simulation()
    sim.step()
