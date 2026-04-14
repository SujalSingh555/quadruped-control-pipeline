import time

from config.robot_config import RobotConfig
from planner.gait_planner import GaitPlanner
from controller.command_manager import CommandManager
from input.joystick import get_input
from utils.conversions import to_degrees, flatten
from comms.sender import send
from utils.visualisation import QuadrupedVisualiser


def main():
    cfg = RobotConfig()

    planner = GaitPlanner(cfg)
    cmd_manager = CommandManager()
    vis = QuadrupedVisualiser(cfg)

    print("Quadruped Control Started...\n")

    last_input = "STOP"

    

   

    while True:
        start_time = time.time()
        
        # 1. Try getting input (non-blocking fallback)
        try:
            user_input = "FORWARD"
            last_input = user_input
        except:
            user_input = last_input  # keep previous command
        #print("INPUT:", user_input)

        # 2. Command update
        command = cmd_manager.update(user_input)
        #print('command:',command)
        planner.set_gait(command)

    
        # 3. Generate gait (returns angles in radians)
        joint_targets = planner.step()
        
        # Save a reference to the raw radian angles exclusively for the visualizer
        joint_targets_rad = joint_targets.copy()

        # 4. Convert to Degrees for the ESP sender
        joint_targets = to_degrees(joint_targets)
        flat = flatten(joint_targets) # Converts dictionary input to a simple list as esp can only accept simple datatype

        # 5. Send to hardware
        send(flat)
        
        # 5.1 Call visualization class simultaneously!
        vis.update_view(joint_targets_rad)

        # 6. Maintain loop rate
        elapsed = time.time() - start_time
        sleep_time = max(0, cfg.dt - elapsed)
        time.sleep(sleep_time)


if __name__ == "__main__":
    main()