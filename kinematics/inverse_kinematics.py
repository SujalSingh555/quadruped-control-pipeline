import numpy as np

class LegIK:
    def __init__(self, config):
        self.L1 = config.L1
        self.L2 = config.L2

    def solve(self, foot_pos):
        x, y, z = foot_pos

        theta0 = 0.0  # hip fixed

        D = (x**2 + z**2 - self.L1**2 - self.L2**2) / (2 * self.L1 * self.L2)
        D = np.clip(D, -1.0, 1.0)

        theta2 = np.arccos(D)

        theta1 = np.arctan2(z, x) - np.arctan2(
            self.L2 * np.sin(theta2),
            self.L1 + self.L2 * np.cos(theta2)
        )

        return np.array([theta0, theta1, theta2])