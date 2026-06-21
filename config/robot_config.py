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
    cycle_time: float = 2
    dt: float = 0.06  # 50 Hz
    # Current target direction; UI sets this dynamically
    target_direction: str = "STOP"

GAITS = {
    "IDLE": {
        "phase_offsets": {"FL": 0, "FR": 0, "BL": 0, "BR": 0}
    },
    "TROT_FORWARD": {
        "phase_offsets": {"FL": 0.0, "BR": 0.0, "FR": 0.5, "BL": 0.5}
    },
    "TURN_LEFT": {
        "phase_offsets": {"FL": 0.0, "BR": 0.0, "FR": 0.5, "BL": 0.5}
    },
    "TURN_RIGHT": {
        "phase_offsets": {"FL": 0.5, "BR": 0.5, "FR": 0.0, "BL": 0.0}
    },
    "TROT_BACKWARD": {
        "phase_offsets": {"FL": 0.0, "BR": 0.0, "FR": 0.5, "BL": 0.5}
    }
}
