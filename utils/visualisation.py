import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets
import numpy as np
import sys
import collections
import time

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
        self.main_win.resize(800, 700)
        
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

class MotorVelocityVisualiser:
    def __init__(self, cfg, history_len=100):
        self.cfg = cfg
        self.history_len = history_len

        # Start Qt application environment
        app = QtWidgets.QApplication.instance()
        if app is None:
            self.app = QtWidgets.QApplication(sys.argv)
        else:
            self.app = app

        # Window 1: Velocity
        self.win_vel = QtWidgets.QWidget()
        self.win_vel.setWindowTitle("Motor Angular Velocity (rad/s) vs Time")
        self.win_vel.resize(1000, 700)
        self.layout_vel = QtWidgets.QVBoxLayout(self.win_vel)
        self.glw_vel = pg.GraphicsLayoutWidget()
        self.layout_vel.addWidget(self.glw_vel)

        # Window 2: Acceleration
        self.win_acc = QtWidgets.QWidget()
        self.win_acc.setWindowTitle("Motor Angular Acceleration (rad/s²) vs Time")
        self.win_acc.resize(1000, 700)
        self.layout_acc = QtWidgets.QVBoxLayout(self.win_acc)
        self.glw_acc = pg.GraphicsLayoutWidget()
        self.layout_acc.addWidget(self.glw_acc)

        self.leg_names = ["FL", "FR", "BL", "BR"]
        self.joint_names = ["Hip", "Thigh", "Knee"]

        self.vel_plots = {}
        self.acc_plots = {}
        self.vel_curves = {}
        self.acc_curves = {}
        
        self.time_history = collections.deque(maxlen=self.history_len)
        self.vel_history = {}
        self.acc_history = {}
        
        # Create a 4x3 grid for both windows
        for i, leg in enumerate(self.leg_names):
            self.vel_history[leg] = [collections.deque(maxlen=self.history_len) for _ in range(3)]
            self.acc_history[leg] = [collections.deque(maxlen=self.history_len) for _ in range(3)]
            for j, joint in enumerate(self.joint_names):
                colors = ['r', 'g', 'b']
                
                # Velocity plot
                p_vel = self.glw_vel.addPlot(title=f"{leg} - {joint}")
                p_vel.setLabel('left', 'Omega', units='rad/s')
                p_vel.setLabel('bottom', 'Time', units='s')
                p_vel.showGrid(x=True, y=True)
                vel_curve = p_vel.plot(pen=pg.mkPen(color=colors[j], width=2))
                self.vel_plots[f"{leg}_{joint}"] = p_vel
                self.vel_curves[f"{leg}_{joint}"] = vel_curve
                
                # Acceleration plot
                p_acc = self.glw_acc.addPlot(title=f"{leg} - {joint}")
                p_acc.setLabel('left', 'Alpha', units='rad/s²')
                p_acc.setLabel('bottom', 'Time', units='s')
                p_acc.showGrid(x=True, y=True)
                acc_curve = p_acc.plot(pen=pg.mkPen(color='w', width=2))
                self.acc_plots[f"{leg}_{joint}"] = p_acc
                self.acc_curves[f"{leg}_{joint}"] = acc_curve
            
            self.glw_vel.nextRow()
            self.glw_acc.nextRow()

        self.win_vel.show()
        self.win_acc.show()

        self.prev_angles = None
        self.prev_omegas = None
        self.prev_time = time.time()
        self.start_time = self.prev_time

    def update_view(self, joint_targets):
        current_time = time.time()
        dt = current_time - self.prev_time
        if dt == 0:
            dt = 1e-6

        t_elapsed = current_time - self.start_time
        self.time_history.append(t_elapsed)

        current_omegas = {}

        for leg in self.leg_names:
            current_angles = joint_targets[leg]
            if self.prev_angles is None:
                omegas = [0.0, 0.0, 0.0]
            else:
                omegas = [(current_angles[k] - self.prev_angles[leg][k]) / dt for k in range(3)]
            
            current_omegas[leg] = omegas

            if self.prev_omegas is None:
                alphas = [0.0, 0.0, 0.0]
            else:
                alphas = [(omegas[k] - self.prev_omegas[leg][k]) / dt for k in range(3)]

            for k, joint in enumerate(self.joint_names):
                self.vel_history[leg][k].append(omegas[k])
                self.acc_history[leg][k].append(alphas[k])
                
                self.vel_curves[f"{leg}_{joint}"].setData(
                    list(self.time_history), 
                    list(self.vel_history[leg][k])
                )
                self.acc_curves[f"{leg}_{joint}"].setData(
                    list(self.time_history), 
                    list(self.acc_history[leg][k])
                )

        self.prev_angles = {leg: list(joint_targets[leg]) for leg in self.leg_names}
        self.prev_omegas = current_omegas
        self.prev_time = current_time

        self.app.processEvents()
