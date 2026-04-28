import numpy as np
import serial
import time

# Initialize once (outside function ideally)
arduino = serial.Serial('COM3', 9600)   # change COM port
time.sleep(2)

def send(joint_array):
    for i in range(int(len(joint_array)/3)):
        joint_array[3*i+1] = -1*(joint_array[3*i+1] + 90)

    print("s", joint_array)

    a = joint_array[1] + 37
    b = joint_array[2] - 90 + 55

    angle = [a, b]

    # 🔥 Convert to string and send
    data_str = f"{angle[0]},{angle[1]}\n"
    arduino.write(data_str.encode())

    print("Sent:", data_str)