import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets
import numpy as np
import sys

from config.robot_config import RobotConfig

class QuadrupedVisualiser:
    def __init__(self, cfg):
        self.cfg = cfg
        self.L1 = cfg.L1
        self.L2 = cfg.L2

        # Start Qt application environment
        app = QtWidgets.QApplication.instance()
        if app is None:
            self.app = QtWidgets.QApplication(sys.argv)
        else:
            self.app = app

        # Main window wrapping both plots and controls
        self.main_win = QtWidgets.QWidget()
        self.main_win.setWindowTitle("Quadruped Leg Forward Kinematics & Controls")
        self.main_win.resize(1000, 900)
        
        self.layout = QtWidgets.QVBoxLayout(self.main_win)
        
        # Plot Widget
        self.win = pg.GraphicsLayoutWidget()
        self.layout.addWidget(self.win)
        
        # Controls Layout
        self.controls_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(self.controls_layout)
        
        # Helper function to add a spinbox
        def add_control(name, min_val, max_val, step, default_val, attr_name):
            vbox = QtWidgets.QVBoxLayout()
            label = QtWidgets.QLabel(name)
            
            spinbox = QtWidgets.QDoubleSpinBox()
            spinbox.setRange(min_val, max_val)
            spinbox.setSingleStep(step)
            spinbox.setValue(default_val)
            
            # Update the configuration dynamically when value changes
            spinbox.valueChanged.connect(lambda v: setattr(self.cfg, attr_name, v))
            
            vbox.addWidget(label)
            vbox.addWidget(spinbox)
            self.controls_layout.addLayout(vbox)

        # Add controls that adjust the gait configuration live!
        add_control("Step Length", 0.01, 0.30, 0.01, self.cfg.step_length, "step_length")
        add_control("Step Height", 0.01, 0.15, 0.01, self.cfg.step_height, "step_height")
        add_control("Cycle Time (s)", 0.2, 5.0, 0.1, self.cfg.cycle_time, "cycle_time")
        
        self.main_win.show()

        self.plots = {}
        self.lines = {}
        self.leg_names = ["FL", "FR", "BL", "BR"]

        # Add time tracking label spanning the top
        self.time_label = self.win.addLabel("Total Elapsed: 0.00s | Bot Time: 0.00s | Delay: 0.00s", col=0, colspan=2)
        self.win.nextRow()

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

        # Add new plots for Velocity and Acceleration of FL leg
        self.win.nextRow()
        
        self.history_len = 100
        self.fl_vel_history = np.zeros((3, self.history_len))
        self.fl_acc_history = np.zeros((3, self.history_len))
        self.prev_fl_angles = None
        self.prev_fl_vel = np.zeros(3)

        self.p_vel = self.win.addPlot(title="FL Velocity (rad/s)")
        self.p_vel.addLegend()
        self.p_vel.showGrid(x=True, y=True)
        self.vel_curves = [
            self.p_vel.plot(pen='r', name="Hip"),
            self.p_vel.plot(pen='g', name="Thigh"),
            self.p_vel.plot(pen='b', name="Knee")
        ]
        
        self.p_acc = self.win.addPlot(title="FL Acceleration (rad/s²)")
        self.p_acc.addLegend()
        self.p_acc.showGrid(x=True, y=True)
        self.acc_curves = [
            self.p_acc.plot(pen='r', name="Hip"),
            self.p_acc.plot(pen='g', name="Thigh"),
            self.p_acc.plot(pen='b', name="Knee")
        ]

    def update_view(self, joint_targets, loop_count=0, total_elapsed=0.0):
        """
        Receives joint_targets from main.py, calculates Forward Kinematics,
        and renders them onto the graph.
        """
        bot_time = loop_count * self.cfg.dt
        delay = total_elapsed - bot_time
        self.time_label.setText(f"<span style='font-size: 16pt; font-weight: bold;'>Total Elapsed: {total_elapsed:.4f}s | Bot Time: {bot_time:.4f}s | Delay: {delay:.4f}s</span>")

        # --- Calculate Velocity & Acceleration out of main.py ---
        fl_angles = np.array(joint_targets["FL"])
        if self.prev_fl_angles is None:
            self.prev_fl_angles = fl_angles

        curr_vel = (fl_angles - self.prev_fl_angles) / self.cfg.dt
        curr_acc = (curr_vel - self.prev_fl_vel) / self.cfg.dt
        
        self.prev_fl_angles = fl_angles
        self.prev_fl_vel = curr_vel
        
        self.fl_vel_history = np.roll(self.fl_vel_history, -1, axis=1)
        self.fl_vel_history[:, -1] = curr_vel
        self.fl_acc_history = np.roll(self.fl_acc_history, -1, axis=1)
        self.fl_acc_history[:, -1] = curr_acc

        for j in range(3):
            self.vel_curves[j].setData(self.fl_vel_history[j])
            self.acc_curves[j].setData(self.fl_acc_history[j])
        # --------------------------------------------------------

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
