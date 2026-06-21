from planner.trajectory import FootTrajectory
from kinematics.inverse_kinematics import LegIK
from planner.gait_library import GAITS

class GaitPlanner:
    def __init__(self, config):
        self.cfg = config
        self.traj = FootTrajectory(config)
        self.ik = LegIK(config)

        self.phase = 0.0   #  replaced time with phase
        self.current_gait = "FORWARD"

    def set_gait(self, gait_name):
        if gait_name in GAITS:
            self.current_gait = gait_name

    def step(self):
        gait = GAITS[self.current_gait]
        joint_targets = {}

        # 1. Base phase update direction (standard: +1, idle: 0)
        phase_direction = 0 if self.current_gait == "IDLE" else 1

        # Update phase
        self.phase += phase_direction * self.cfg.dt
        self.phase = self.phase % self.cfg.cycle_time

        # 2. Compute per-leg motion parameters based on gait mode
        for leg, phase_offset in gait["phase_offsets"].items():
            t_leg = (self.phase + phase_offset * self.cfg.cycle_time) % self.cfg.cycle_time

            # Defaults
            direction = 1
            lateral = 0.0

            # Determine leg-specific direction and lateral values based on current gait
            if "BACKWARD" in self.current_gait:
                direction = -1
            elif self.current_gait == "TURN_LEFT":
                # Left legs (FL, BL) go backward, right legs (FR, BR) go forward to rotate CCW
                direction = -1 if leg in ["FL", "BL"] else 1
            elif self.current_gait == "TURN_RIGHT":
                # Left legs (FL, BL) go forward, right legs (FR, BR) go backward to rotate CW
                direction = 1 if leg in ["FL", "BL"] else -1
            elif self.current_gait == "IDLE":
                direction = 0

            foot_pos = self.traj.evaluate(
                t_leg,
                direction=direction,
                lateral=int(lateral)
            )

            joint_targets[leg] = self.ik.solve(foot_pos)

        return joint_targets