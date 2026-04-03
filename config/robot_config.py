from dataclasses import dataclass

@dataclass
class RobotConfig:
    # Geometry
    L1: float = 0.10   # thigh
    L2: float = 0.10   # calf

    # Gait parameters
    step_length: float = 0.10
    step_height: float = 0.04
    body_height: float = 0.18

    # Timing
    cycle_time: float = 1.0
    dt: float = 0.02  # 50 Hz