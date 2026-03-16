import numpy as np

from sound import *

class Cannon:
    def __init__(self, pos, model_base, model_barrel,
                 muzzle_vel, load_time, limit_el):
        self.pos = pos
        self.model_base = model_base
        self.model_barrel = model_barrel
        self.muzzle_vel_max = muzzle_vel
        self.load_time = load_time
        self.limit_el = limit_el

        self.base_orient = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        self.barrel_orient = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

        self.az = 0
        self.el = self.limit_el[0]
        self.charges = 3
        self.max_charges = 5
        self.load_state = 1

        self.az_rate = 0.1
        self.el_rate = 0.1

        self.charge_cooldown = 0

    def update(self, d_az, d_el, d_charge, shoot, dt):
        self.rotate(d_az * dt, d_el * dt)

        if d_charge != 0 and 1 <= self.charges + d_charge <= self.max_charges and self.charge_cooldown <= 0:
            self.charges += d_charge
            self.charge_cooldown = 0.5
            play_sfx("prop_load", 0, 3, 1)

        if self.load_state < 1:
            self.load_state += dt / self.load_time

        if self.load_state > 1:
            self.load_state = 1
            play_sfx("shell_load", 0, 4, 1)

        if shoot:
            self.shoot()

        if self.az < 0:
            self.az += np.deg2rad(360)
        elif self.az > np.deg2rad(360):
            self.az -= np.deg2rad(360)

        if self.charge_cooldown > 0:
            self.charge_cooldown -= dt

    def rotate(self, d_az, d_el):
        self.az += d_az * self.az_rate
        self.el += d_el * self.el_rate

        if self.el < self.limit_el[0]:
            self.el = self.limit_el[0]
        elif self.el > self.limit_el[1]:
            self.el = self.limit_el[1]

        self.base_orient = self.calculateOrientationMatrixBase()
        self.barrel_orient = self.calculateOrientationMatrixBarrel()

    def shoot(self):
        if self.load_state >= 1:
            self.load_state = 0

    def calculateOrientationMatrixBase(self):
        yaw_matrix = np.array([[np.cos(self.az), 0, np.sin(self.az)],
                               [0, 1, 0],
                               [-np.sin(self.az), 0, np.cos(self.az)]])

        pitch_matrix = np.array([[1, 0, 0],
                                 [0, 1, 0],
                                 [0, 0, 1]])

        orientation_matrix = np.dot(pitch_matrix, yaw_matrix)
        return orientation_matrix

    def calculateOrientationMatrixBarrel(self):
        yaw_matrix = np.array([[np.cos(self.az), 0, np.sin(self.az)],
                               [0, 1, 0],
                               [-np.sin(self.az), 0, np.cos(self.az)]])

        pitch_matrix = np.array([[1, 0, 0],
                                 [0, np.cos(self.el), np.sin(self.el)],
                                 [0, -np.sin(self.el), np.cos(self.el)]])

        orientation_matrix = np.dot(pitch_matrix, yaw_matrix)
        return orientation_matrix

class Shell:
    def __init__(self, mass, diam, pos, vel, drag_coeff):
        self.mass = mass
        self.diam = diam
        self.pos = pos
        self.vel = vel
        self.drag_coeff = drag_coeff

    def update(self, dt):
        a_grav = np.array([0, -9.80655, 0])
        a_drag = 0.5 * self.drag_coeff * 1 * (0.25 * np.pi * self.diam**2) * np.linalg.norm(self.vel)**2
        a_drag *= -self.vel / np.linalg.norm(self.vel)
        
        self.vel += (a_grav + a_drag) * dt
        self.pos += self.vel * dt

    def check_collisions(self, objs):
        pass

class Splash:
    def __init__(self, pos, model):
        self.pos = pos
        self.model = model
        self.state = 0
        self.time_end = 2
        self.orient = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

    def update(self, dt):
        self.state += dt
