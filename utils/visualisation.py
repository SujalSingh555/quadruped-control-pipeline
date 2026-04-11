import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets
import numpy as np
import sys

from config.robot_config import RobotConfig

class QuadrupedVisualiser:
    def __init__(self, cfg):
        self.L1 = cfg.L1
        self.L2 = cfg.L2

        # Start Qt application environment
        app = QtWidgets.QApplication.instance()
        if app is None:
            self.app = QtWidgets.QApplication(sys.argv)
        else:
            self.app = app

        self.win = pg.GraphicsLayoutWidget(show=True, title="Quadruped Leg Forward Kinematics")
        self.win.resize(800, 600)

        self.plots = {}
        self.lines = {}
        self.leg_names = ["FL", "FR", "BL", "BR"]

        # Create 4 plots for 4 legs (2x2 grid as you preferred)
        for i, leg in enumerate(self.leg_names):
            p = self.win.addPlot(title=f"Leg: {leg}")
            p.setXRange(-0.2, 0.2)
            p.setYRange(-0.3, 0.1) # Assuming z is downwards, from 0 to -0.3
            p.setAspectLocked(True)
            p.showGrid(x=True, y=True)
            
            # We will plot 3 points: Hip, Knee, Foot -> 2 line segments
            line = p.plot([], [], pen=pg.mkPen('w', width=3), symbol='o', symbolSize=8, symbolBrush='b')
            self.lines[leg] = line
            
            if i == 1:
                self.win.nextRow()

    def update_view(self, joint_targets):
        """
        Receives joint_targets from main.py, calculates Forward Kinematics,
        and renders them onto the graph.
        """
        for leg in self.leg_names:
            angles = joint_targets[leg]
            # angles[0] = theta0, angles[1] = theta1 (thigh pitch), angles[2] = theta2 (knee pitch)
            theta1 = angles[1]
            theta2 = angles[2]
            
            # Forward Kinematics (in X-Z plane)
            # Keeping the hips at 0.0 as requested
            x_hip = 0.0
            z_hip = 0.0
            
            x_knee = self.L1 * np.cos(theta1)
            z_knee = self.L1 * np.sin(theta1)
            
            x_foot = x_knee + self.L2 * np.cos(theta1 + theta2)
            z_foot = z_knee + self.L2 * np.sin(theta1 + theta2)
            
            # Update plot
            self.lines[leg].setData([x_hip, x_knee, x_foot], [z_hip, z_knee, z_foot])
            
        # Process PyQT events to instantly render without blocking the main.py loop
        self.app.processEvents()
