from config.robot_config import RobotConfig
from planner.gait_planner import GaitPlanner

cfg = RobotConfig()
planner = GaitPlanner(cfg)

for i in range(10):
    print(planner.step())