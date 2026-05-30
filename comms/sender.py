import numpy as np
import time

# Initialize once (outside function ideally)
arduino = None
serial_available = False

try:
    import serial
    try:
        arduino = serial.Serial('COM3', 9600)   # change COM port
        time.sleep(2)
        serial_available = True
        print("Serial interface initialized on COM3.")
    except Exception as e:
        print(f"Serial port not available: {e}. Serial communication is disabled.")
except ImportError:
    print("pyserial is not installed. Serial communication is disabled.")

def send(joint_array):
    for i in range(int(len(joint_array)/3)):
        joint_array[3*i+1] = -1*(joint_array[3*i+1] + 90)

    

    a = joint_array[1] 
    b = joint_array[2] 

    angle = [a, b]

    #  Convert to string and send if serial hardware is present
    if serial_available and arduino is not None:
        data_str = f"{angle[0]},{angle[1]}\n"
        try:
            arduino.write(data_str.encode())
            print("Sent:", data_str.strip())
        except Exception as e:
            print(f"Error writing to serial: {e}")
