# Combined input retrieval and command mapping

def get_input():
    # TEMP: replace later with real joystick
    pass
    """cmd = input("Enter command (f/b/l/r/s): ").strip().lower()

    if cmd == "f":
        return "FORWARD"
    elif cmd == "b":
        return "BACKWARD"
    elif cmd == "l":
        return "LEFT"
    elif cmd == "r":
        return "RIGHT"
    elif cmd == "s":
        return "STOP"
    else:
        return "STOP"
    """

class CommandManager:
    def __init__(self):
        self.current_command = "IDLE"

    def update(self, joystick_input):
        mapping = {
            "FORWARD": "TROT_FORWARD",
            "BACKWARD": "TROT_BACKWARD",
            "LEFT": "TURN_LEFT",
            "RIGHT": "TURN_RIGHT",
            "STOP": "IDLE",
            "WALK":"WALK",
            "PACE":"PACE",
            "BOUND":"BOUND"
        }

        key = joystick_input.upper().strip()

        self.current_command = mapping.get(key, "IDLE")
        return self.current_command
