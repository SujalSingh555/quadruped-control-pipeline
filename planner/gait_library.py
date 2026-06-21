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
    ,
    "PACE": {
        # Lateral sequence: left legs move together, right legs together
        "phase_offsets": {"FL": 0.0, "BL": 0.0, "FR": 0.5, "BR": 0.5}
    },
    "BOUND": {
        # Front legs together, hind legs together (bound)
        "phase_offsets": {"FL": 0.0, "FR": 0.0, "BL": 0.5, "BR": 0.5}
    }
    ,
    "WALK": {
        "phase_offsets": {"FL": 0.0, "FR": 0.25, "BR": 0.5, "BL": 0.75}
    },
    
    "PACE": {
        # Same-side (lateral) pairs move together.
        # The entire left side moves, then the entire right side moves.
        "phase_offsets": {"FL": 0.0, "BL": 0.0, "FR": 0.5, "BR": 0.5}
    },
    
    "BOUND": {
        # Front vs. Rear pairing.
        # Both front legs swing together, then both rear legs swing together.
        "phase_offsets": {"FL": 0.0, "FR": 0.0, "BL": 0.5, "BR": 0.5}
    }
}
