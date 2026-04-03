import numpy as np

class FootTrajectory:
    def __init__(self, config):
        self.cfg = config

    def evaluate(self, t, direction=1, lateral=0):
        T = self.cfg.cycle_time
        L = self.cfg.step_length
        h = self.cfg.step_height
        z0 = -self.cfg.body_height

        half_T = T / 2

        if t < half_T:
            # STANCE
            x = direction*(L/2 - L) * (t / half_T)
            z = z0
        else:
            # SWING
            s = (t - half_T) / half_T
            x = direction*(-L/2 + L * s)
            z = z0 + h * np.sin(np.pi * s)

        return np.array([x, 0.0, z])