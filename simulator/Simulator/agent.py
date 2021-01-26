from .grid import Grid
import numpy as np

class Agent:
    id=0
    def __init__(self, grid:Grid, pos, goal_name, to_flight=None) -> None:
        self.path = grid.paths[goal_name]
        self.speed = 1*60
        self.grid = grid
        self.pos = pos
        self.velocity = np.zeros(2)
        self.in_bounds = True
        self.grid_pos = pos
        self.destination = grid.goals[goal_name]
        self.goal_name = goal_name
        self.to_flight = to_flight
        self.id = Agent.id + 1
        Agent.id += 1

    def reached_goal(self):
        return (self.pos[0]-self.destination[0])**2 + (self.pos[1]-self.destination[1])**2 < 100

    def preferred_velocity(self):
        def normalize(v):
            norm = np.linalg.norm(v)
            if norm == 0:
                return v
            return v / norm

        grid_pos, self.in_bounds = self.grid.pos_to_grid(tuple(self.pos))
        next_pos = self.path[tuple(grid_pos)]
        vec = normalize(
            np.array([next_pos[0]-grid_pos[0], next_pos[1]-grid_pos[1]]))*self.speed

        # if self.reached_goal():
        #     return np.zeros(2)

        return vec

    def get_pos(self):
        return (self.pos[0]/self.grid.grid_size[0], self.pos[1]/self.grid.grid_size[1])