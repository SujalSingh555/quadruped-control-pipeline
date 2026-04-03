class CommandManager:
    def __init__(self):
        self.current_command = "IDLE"

    def update(self, joystick_input):
        if joystick_input == "FORWARD":
            self.current_command = "TROT_FORWARD"
        elif joystick_input == "LEFT":
            self.current_command = "TURN_LEFT"
        elif joystick_input == "RIGHT":
            self.current_command = "TURN_RIGHT"
        else:
            self.current_command = "IDLE"

        return self.current_command