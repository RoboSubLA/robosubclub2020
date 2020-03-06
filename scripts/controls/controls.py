from pid import PID
from angle_optimization import angle_optimization

X_PID_CONSTANTS = (100, 100, 100)
Y_PID_CONSTANTS = (100, 100, 100)
Z_PID_CONSTANTS = (100, 100, 100)
H_PID_CONSTANTS = (100, 100, 100)
DEPTH_PID_CONSTANTS = (100, 100, 100)
VERT_PID_CONSTANTS = (100, 100, 100)

#dictionary for pins on the Sub
sub_pins = {'front_left':1, 'front_right':2, 'back_left':3, 'back_right':4, 'left_h': 5, 'right_h':6}


#in charge of only the vertical componenet of the sub
# adding a comment here - r2

class Vertical_Controller:
    def __init__(self, front_left_pin, front_right_pin, back_left_pin, back_right_pin, v_pid_konstants, y_pid_konstants, z_pid_konstants,
                 v_setpoint = 0, y_setpoint = 0, z_setpoint = 0):
        self.front_left = Thruster_Controller(front_left_pin)
        self.front_right = Thruster_Controller(front_right_pin)
        self.back_left = Thruster_Controller(back_left_pin)
        self.back_right = Thruster_Controller(back_right_pin)

        #create PID controllers with defaults
        self.v_pid = PID()
        self.y_pid = PID()
        self.z_pid = PID()

        #set the initial setpoints
        self.set_setpoints(v_setpoint, y_setpoint, z_setpoint)

        #set the kp, ki, and kd
        self.v_pid.tunings(v_pid_konstants[0],v_pid_konstants[1],v_pid_konstants[2])
        self.y_pid.tunings(y_pid_konstants[0],y_pid_konstants[1],y_pid_konstants[2])
        self.z_pid.tunings(z_pid_konstants[0],z_pid_konstants[1],z_pid_konstants[2])


    def set_setpoints(self, v_setpoint, y_setpoint = 0, z_setpoint = 0):
        self.v_setpoint = v_setpoint
        self.y_setpoint = y_setpoint
        self.z_setpoint = z_setpoint

        self.v_pid.set_setpoint(v_setpoint)
        self.y_pid.set_setpoint(y_setpoint)
        self.z_pid.set_setpoint(z_setpoint)

    def __call__(self, v_current, y_current, z_current):
        # this is where the mixer is added in to the stuff

        # calculaion to reframe the problem
        real_y_setpoint = angle_optimization(y_current)
        real_z_setpoint = angle_optimization(z_current)
        y_current = 0
        z_current = 0

        # update the setpoints, and input to the modified values
        self.set_setpoints(self.v_setpoint, real_y_setpoint, real_z_setpoint)

        # calculate the new outputs
        # make sure they are within defined limits
        v_output = self.linear_limit(self.h_pid(v_current))
        y_output = self.angular_limit(self.y_pid(y_current))
        z_output = self.angular_limit(self.z_pid(z_current))

        # mix the values
        outputs = self.mixer(v_output, y_output, z_output)

        # send the modified signals to the thrusters
        self.front_left.set_pwm(outputs[0])
        self.front_right.set_pwm(outputs[1])
        self.back_left.set_pwm(outputs[2])
        self.back_right.set_pwm(outputs[3])

    def mixer(self, v_output, y_output, z_output):
        neutral = 1500
        front_right = neutral + v_output + y_output + z_output
        front_left = neutral + v_output - y_output + z_output
        back_left = neutral + v_output - y_output - z_output
        back_right = neutral + v_output + y_output - z_output

        return (front_left, front_right, back_left, back_right)

    def linear_limit(self, value):
        if value > self.linear_max:
            return self.linear_max
        if value < self.linear_min:
            return self.linear_min
        return value

    def angular_limit(self, value):
        if value > self.angular_max:
            return self.angular_max
        if value < self.angular_min:
            return self.angular_min
        return value


class Horizontal_Controller:
    def __init__(self, left_thruster, right_thruster):
        #TODO
        #needs to be updated with new values for thrusters
        #-1 to 1

        #set limits to default
        self.linear_max, self.linear_min = 1800, 1200
        self.angular_max, self.angular_min = 1800, 1200

        self.left_thruster = left_thruster
        self.right_thruster = right_thruster

        self.angle_setpoint = 0
        self.hor_setpoint = 0

        #create PID controllers with defaults
        self.h_pid = PID()
        self.a_pid = PID()

        #set the kp, ki, and kd
        self.h_pid.tunings(H_PID_CONSTANTS[0], H_PID_CONSTANTS[1], H_PID_CONSTANTS[2])
        self.a_pid.tunings(X_PID_CONSTANTS[0], X_PID_CONSTANTS[1], X_PID_CONSTANTS[2])

        #set the setpoints
        self.set_setpoints(hor_setpoint, angle_setpoint)

    def __call__(self, h_current, a_current):
        #this is where the mixer is added in to the stuff

        #calculaion to reframe the problem
        real_angle_setpoint = angle_optimization(a_current)
        a_current = 0

        #update the setpoints, and input to the modified values
        self.set_setpoints(0, real_angle_setpoint)

        #calculate the new outputs
        #make sure they are wihin the defined limits
        h_output = self.linear_limit(self.h_pid(h_current))
        a_output = self.angular_limit(self.a_pid(a_current))

        #mix the values
        outputs = self.mixer(h_output, a_output)

        #send the modified signals to the thrusters
        self.left_thruster.set_pwm(outputs[0])
        self.right_thruster.set_pwm(outputs[1])

    def set_setpoints(self, hor_setpoint, angle_setpoint):
        self.hor_setpoint = hor_setpoint
        self.angle_setpoint = angle_setpoint

        # set the setpoints
        self.h_pid.set_setpoint(self.hor_setpoint)
        self.a_pid.set_setpoint(self.angle_setpoint)

    def mixer(self, h_output, a_output):
        #set the neutral on the pwm signal
        neutral = 1500
        left_output = neutral + h_output + a_output
        right_output = neutral + h_output - a_output
        return (left_output, right_output)

    def set_limits(self, linear_limits, angular_limits):
        self.linear_min = linear_limits[0]
        self.linear_max = linear_limits[1]

        self.angular_min = angular_limits[0]
        self.angular_max = angular_limits[1]

    def linear_limit(self, value):
        if value > self.linear_max:
            return self.linear_max
        if value < self.linear_min:
            return self.linear_min
        return value

    def angular_limit(self, value):
        if value > self.angular_max:
            return self.angular_max
        if value < self.angular_min:
            return self.angular_min
        return value


class Sub_Controller:
    def __init__(self):
        thruster = init_thrusters()

        self.h_controller = Horizontal_Controller(thruster['left_h'], thruster['right_h'])
        self.v_controller = Vertical_Controller(thruster['front_left'], thruster['front_right'],
                                                thruster['back_left'], thruster['back_right'])

    def set_setpoints(self, h_setpoint, v_setpoint, x_setpoint, y_setpoint, z_setpoint):
        self.h_controller(h_setpoint, x_setpoint)
        self.v_controller(v_setpoint, y_setpoint, z_setpoint)

    def __call__(self, h_current, v_current, x_current, y_current, z_current):
        self.h_controller(h_current, x_current)
        self.v_controller(v_current, y_current, z_current)


    #find out how this works
    def set_limits(self, linear_limits, angular_limits):
        self.h_controller.set_limits(linear_limits, angular_limits)
        self.v_controller.set_limits(linear_limits, angular_limits)

    #init the thrusters
    def init_thrusters(self):
        kit = Servokit(channels=16)
        for s in kit:
            s.set_pulse_width_range(min_pwm, max_pwm)

        thrusters = {}
        for t in thruster_pins:
            thrusters[t] = kit[thruster_pins[t]]

        return thrusters
