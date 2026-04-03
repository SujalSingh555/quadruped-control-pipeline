# TEMP: replace later with real joystick

def get_input():
    cmd = input("Enter command (f/b/l/r/s): ").strip().lower()

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