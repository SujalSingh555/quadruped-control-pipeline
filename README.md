#  Quadruped Gait Planner (From Scratch)

This project implements a **phase-based quadruped locomotion system** from scratch.

Instead of directly controlling joint angles, the system generates motion through:

- phase-driven gait timing  
- foot trajectory generation (linear + sinusoidal)  
- inverse kinematics (IK)  
- modular planner → trajectory → IK pipeline  

---

##  Core Pipeline

```
phase → per-leg timing → foot trajectory → inverse kinematics → joint angles
```

Everything is controlled using a **single phase variable**.

---

##  Gait Planner

Main logic lives in `GaitPlanner`.

### Initialization

```python
self.phase = 0.0
self.current_gait = "IDLE"
```

---

##  Step Function (Main Loop)

```python
def step(self):
```

This runs one iteration of the gait cycle.

---

### 1. Direction Control

```python
if "BACKWARD" in self.current_gait:
    direction = -1
else:
    direction = 1
```

✔ Clean trick:  
No separate logic needed for backward motion  
→ just reverse phase evolution  

---

### 2. Phase Update (MOST IMPORTANT)

```python
self.phase += direction * self.cfg.dt
self.phase = self.phase % self.cfg.cycle_time
```

This makes motion:
- cyclic  
- continuous  
- direction-dependent  

---

### 3. Per-Leg Phase Shift

Each leg has its own offset:

```python
t_leg = (self.phase + phase_offset * self.cfg.cycle_time) % self.cfg.cycle_time
```

This is what creates **different gaits**.

---

##  Gait Design

Defined in:

```
planner/gait_library.py
```

Each gait specifies:

```python
GAITS = {
    "TROT": {
        "phase_offsets": {
            "FL": 0.0,
            "RR": 0.0,
            "FR": 0.5,
            "RL": 0.5,
        }
    }
}
```

---

###  Example: TROT Gait

- Diagonal legs move together  
- Phase difference = 0.5 (half cycle)

```
FL + RR → stance/swing together
FR + RL → opposite phase
```

This creates:
- dynamic balance  
- symmetric motion  

---

##  Foot Trajectory

Handled in:

```
planner/trajectory.py → FootTrajectory
```

---

### Motion Split

Each cycle is divided into:

---

###  Stance Phase

```python
x = direction * (L/2 - L * (t / (T/2)))
z = z0
```

✔ linear motion  
✔ foot on ground  
✔ generates propulsion  

---

###  Swing Phase

```python
s = (t - T/2) / (T/2)

x = direction * (-L/2 + L * s)
z = z0 + h * sin(pi * s)
```

✔ linear forward motion (x)  
✔ sinusoidal lift (z)  

This combination is the key:
- smooth motion  
- no jerks  
- natural stepping  

---

##  Important Detail

Inside planner:

```python
foot_pos = self.traj.evaluate(
    t_leg,
    direction=1,
    lateral=lateral
)
```

Even though planner computes direction:

 trajectory direction is kept **1 intentionally**

Reason:
- phase direction already controls forward/backward  
- avoids double flipping  

---

##  Inverse Kinematics

Handled in:

```
kinematics/inverse_kinematics.py
```

---

### Equations

Given foot position `(x, y, z)`:

```python
D = (x**2 + z**2 - L1**2 - L2**2) / (2 * L1 * L2)
D = np.clip(D, -1.0, 1.0)

theta2 = np.arccos(D)

theta1 = np.arctan2(z, x) - np.arctan2(
    L2 * np.sin(theta2),
    L1 + L2 * np.cos(theta2)
)
```

```python
theta0 = 0.0
```

✔ planar 2-link leg  
✔ stable IK solution  

---

##  Project Structure

```
config/         → parameters (step length, height, cycle time)
planner/        → gait planner + trajectory
kinematics/     → inverse kinematics
controller/     → joint command logic
input/          → user input
utils/          → helper functions
tests/          → testing
main.py         → entry point
```

---

##  Running

```bash
python main.py
```

---

##  Output

- joint targets per leg  
- debug logs:
  - phase  
  - direction  
  - current gait  

---

##  Current Features

✔ Phase-based gait system  
✔ Trot gait implementation  
✔ Forward + backward motion  
✔ Foot trajectory (linear + sin)  
✔ Inverse kinematics  

---

##  Next Improvements

- Add lateral motion (y-axis)  
- More gaits (walk, bound, gallop)  
- Stability control  
- Dynamic step adaptation  

---

##  Key Insight

> Quadruped walking is not about joint angles  
> it's about **timing + foot trajectory**

Once trajectory is correct:
- IK handles joints  
- gait emerges naturally  

---

##  Author

Sujal Singh  
Mechanical Engineering @ IIT Kharagpur  
Robotics | Control | ML
