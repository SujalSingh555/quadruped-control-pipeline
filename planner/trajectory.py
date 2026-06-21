import numpy as np

class FootTrajectory:
    def __init__(self, config):
        self.cfg = config

    def evaluate(self, t, direction=1, lateral=0):
        T = self.cfg.cycle_time
        L = self.cfg.step_length
        h = self.cfg.step_height
        z0 = -self.cfg.body_height

        # ---------------- OLD TRAJECTORY ----------------
        
        """theta = 2*np.pi*t/T

        x = -direction*(L/2)*np.cos(theta)
        z = z0 + h*max(0, np.sin(theta))"""

        
        
        # ---------------- BEZIER TRAJECTORY ----------------

        s = (t % T) / T

        if s < 0.5:
            # STANCE PHASE
            u = s / 0.5
            x = direction * (L/2 - L*u)
            z = z0

        else:
            # SWING PHASE
            u = (s - 0.5) / 0.5

            P0 = np.array([-L/2, z0])
            P1 = np.array([-L/2, z0 + h])
            P2 = np.array([ L/2, z0 + h])
            P3 = np.array([ L/2, z0])

            B = ((1-u)**3)*P0 + 3*((1-u)**2)*u*P1 + 3*(1-u)*(u**2)*P2 + (u**3)*P3

            x = direction * B[0]
            z = B[1]

        return np.array([x, lateral, z])