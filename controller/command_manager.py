class CommandManager:
    def __init__(self):
        self.current_command = "IDLE"

    def update(self, joystick_input):
        mapping = {
            "FORWARD": "TROT_FORWARD",
            "BACKWARD": "TROT_BACKWARD",
            "LEFT": "TURN_LEFT",
            "RIGHT": "TURN_RIGHT",
            "STOP": "IDLE"
        }

        key = joystick_input.upper().strip()

        self.current_command = mapping.get(key, "IDLE")
        return self.current_command