'''contains code to convert the controls commands to output signals to the thriusters

Must be tested on the raspberri pi connected to the PWM external board
'''
from adafruit_servokit import ServoKit

#adafruit output functions on thruster values from -1 to 1


#define min and max PWM signal
min_pwm = 1000
max_pwm = 2000

class Servo(Servokit):
    def __init__(self):
        self.super(channels=16)
        self.set_range_pwm()
        #kit.servo[0].set_pulse_width_range(1000, 2000)

    def set_range_pwm(self):
        for s in self.servo:
            s.set_pulse_width_range(min_pwm, max_pwm)