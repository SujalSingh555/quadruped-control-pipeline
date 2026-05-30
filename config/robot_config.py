from dataclasses import dataclass

@dataclass
class RobotConfig:
    # Geometry
    L1: float = 0.14   # thigh
    L2: float = 0.153   # calf

    # Gait parameters
    step_length: float = 0.2
    step_height: float = 0.04
    body_height: float = 0.25

    # Timing
    cycle_time: float = 1
    dt: float = 0.06  # 50 Hz