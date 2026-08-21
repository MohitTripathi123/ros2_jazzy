

def validation_speed(speed):
    if speed < 0:
        raise ValueError("Speed cannot be negative.")
    elif speed > 100:
        raise ValueError("Speed cannot exceed 100.")
    return True