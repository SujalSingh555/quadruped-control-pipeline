import numpy as np

def to_degrees(joint_targets):
    return {
        leg: np.degrees(angles)
        for leg, angles in joint_targets.items()
    }

def flatten(joint_targets):
    order = ["FL", "FR", "BL", "BR"]
    flat = []

    for leg in order:
        flat.extend(joint_targets[leg])

    return np.array(flat)