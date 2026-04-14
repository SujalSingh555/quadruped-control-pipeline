# comms/sender.py

import numpy as np

def send(joint_array):
    global log_data
    for i in range(int((len(joint_array)/3))):    #angles are taken from -pi/2 to body and clockwise converted to positive sign 
        joint_array[3*i+1]=-1*(joint_array[3*i+1]+90)
    #joint_array[1]=-1*(joint_array[1]+90)
    #joint_array[4]=-1*(joint_array[4]+90)
    #joint_array[7]=-1*(joint_array[7]+90) 
    #joint_array[10]=-1*(joint_array[10]+90)   
    print("Sending:", joint_array)
    