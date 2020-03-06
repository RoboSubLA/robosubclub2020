# converts and angle to a usable form
def angle_optimization(self: object, a_current: int) -> int:
    angle_error = self.angle_setpoint - a_current
    return angle_converter(angle_error)


def angle_converter(angle):
    """
    :type angle: integer
    """
    if angle > 180:
        return angle - 360
    elif angle < -180:
        return angle + 360
    else:
        return angle