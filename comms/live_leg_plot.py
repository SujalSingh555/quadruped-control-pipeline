import numpy as np
import matplotlib.pyplot as plt
import time
import os

plt.ion()
fig, ax = plt.subplots()

FILE = "joint_log.npy"

# 🔥 link lengths (same as your IK config)
L1 = 0.1   # thigh
L2 = 0.1   # calf

def forward_kinematics(theta1, theta2):
    """
    Convert joint angles → foot position
    (2D planar leg: thigh + calf)
    """
    x = L1 * np.cos(theta1) + L2 * np.cos(theta1 + theta2)
    z = L1 * np.sin(theta1) + L2 * np.sin(theta1 + theta2)
    return x, z


while True:
    if not os.path.exists(FILE):
        print("Waiting for data...")
        time.sleep(1)
        continue

    try:
        data = np.load(FILE)

        if len(data) < 5:
            continue

        # 🔥 take last 200 points
        data = data[-200:]

        x_list = []
        z_list = []

        for row in data:
            # 🔥 pick one leg (FL)
            hip = np.deg2rad(row[0])
            thigh = np.deg2rad(row[1])
            knee = np.deg2rad(row[2])

            # ignore hip for now (2D motion)
            x, z = forward_kinematics(thigh, knee)

            x_list.append(x)
            z_list.append(z)

        ax.clear()

        # 🔥 trajectory path
        ax.plot(x_list, z_list, label="Foot Path")

        # 🔥 current foot position
        ax.scatter(x_list[-1], z_list[-1], color='red')

        ax.set_title("Foot Trajectory (Leg Motion)")
        ax.set_xlabel("X (forward)")
        ax.set_ylabel("Z (height)")
        ax.legend()
        ax.grid()

        ax.set_aspect('equal')

        plt.pause(0.01)

    except Exception as e:
        print("Error:", e)

    time.sleep(0.05)