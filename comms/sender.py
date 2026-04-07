# comms/sender.py

import numpy as np

log_data = []

def send(joint_array):
    global log_data

    print("Sending:", joint_array)

    log_data.append(joint_array.copy())

    # 🔥 overwrite file continuously
    np.save("joint_log.npy", np.array(log_data))