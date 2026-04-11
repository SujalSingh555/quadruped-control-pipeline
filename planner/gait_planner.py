from planner.trajectory import FootTrajectory
from kinematics.inverse_kinematics import LegIK
from planner.gait_library import GAITS

class GaitPlanner:
    def __init__(self, config):
        self.cfg = config
        self.traj = FootTrajectory(config)
        self.ik = LegIK(config)

        self.phase = 0.0   # 🔥 replaced time with phase
        self.current_gait = "IDLE"

    def set_gait(self, gait_name):
        if gait_name in GAITS:
            self.current_gait = gait_name

    def step(self):
        gait = GAITS[self.current_gait]
        joint_targets = {}

        # 🔥 1. Decide direction
        if "BACKWARD" in self.current_gait:
            direction = -1
        else:
            direction = 1

        #print ("direction:",direction)

        # 🔥 2. Update phase (THIS IS THE KEY FIX)
        self.phase += direction * self.cfg.dt
        self.phase = self.phase % self.cfg.cycle_time

        # (future: sideways)
        lateral = 0

        # 🔥 3. Compute per-leg motion
        for leg, phase_offset in gait["phase_offsets"].items():
            t_leg = (self.phase + phase_offset * self.cfg.cycle_time) % self.cfg.cycle_time

            foot_pos = self.traj.evaluate(
                t_leg,
                direction=1,      # ⚠️ IMPORTANT: keep this 1 now
                lateral=lateral
            )

            joint_targets[leg] = self.ik.solve(foot_pos)
        #print("GAIT:", repr(self.current_gait))

        return joint_targets