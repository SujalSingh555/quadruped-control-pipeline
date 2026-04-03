# TEMP: replace later with real joystick

def get_input():
    cmd = input("Enter command (f/l/r/s): ").strip()

    if cmd == "f":
        return "FORWARD"
    elif cmd == "l":
        return "LEFT"
    elif cmd == "r":
        return "RIGHT"
    else:
        return "STOP"