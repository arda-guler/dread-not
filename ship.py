import numpy as np
import copy

class Ship:
    def __init__(self, model, pos, vel):
        self.model = model
        self.pos = pos
        self.vel = vel

        self.az = np.arctan2(self.vel[1], self.vel[0])
        self.orient = self.calculateOrientationMatrixBase()

        self.smokes = []
        self.last_smoke_time = 0

        self.state = 0

    def update(self, rot, dt):
        self.pos += self.vel * dt
        self.az = np.arctan2(self.vel[1], self.vel[0])
        self.orient = self.calculateOrientationMatrixBase()

    def calculateOrientationMatrixBase(self):
        yaw_matrix = np.array([[np.cos(self.az), 0, np.sin(self.az)],
                               [0, 1, 0],
                               [-np.sin(self.az), 0, np.cos(self.az)]])

        pitch_matrix = np.array([[1, 0, 0],
                                 [0, 1, 0],
                                 [0, 0, 1]])

        orientation_matrix = np.dot(pitch_matrix, yaw_matrix)
        return orientation_matrix

class ShipSmoke:
    def __init__(self, ship):
        self.ship = ship
        self.pos = copy.copy(ship.pos) + np.array([0, 15, 0])
        self.vel = np.array([0, 3, 0])
        self.time_end = 15
        self.state = 0

    def update(self, dt):
        self.pos += self.vel * dt
        self.state += dt
