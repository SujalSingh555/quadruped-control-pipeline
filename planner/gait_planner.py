from planner.trajectory import FootTrajectory
from kinematics.inverse_kinematics import LegIK
from planner.gait_library import GAITS

class GaitPlanner:
    def __init__(self, config):
        self.cfg = config
        self.traj = FootTrajectory(config)
        self.ik = LegIK(config)

        self.time = 0.0
        self.current_gait = "IDLE"

    def set_gait(self, gait_name):
        if gait_name in GAITS:
            self.current_gait = gait_name

    def step(self):
        self.time += self.cfg.dt

        gait = GAITS[self.current_gait]
        joint_targets = {}

        for leg, phase in gait["phase_offsets"].items():
            t_leg = (self.time + phase * self.cfg.cycle_time) % self.cfg.cycle_time

            foot_pos = self.traj.evaluate(t_leg)
            joint_targets[leg] = self.ik.solve(foot_pos)

        return joint_targets