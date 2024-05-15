#Variant 3
from math import *
class Robot:
    def __init__(self, x, y, velocity, angle):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.angle = angle

    def forward(self, time_in_seconds):
        self.time_in_seconds = time_in_seconds
        self.x += self.velocity*time_in_seconds*cos(self.angle*pi/180)
        self.y += self.velocity*time_in_seconds*sin(self.angle*pi/180)
        print('Coordinates of the robot:', self.x, self.y)
    def rotate(self, rotate_angle):
        self.rotate_angle = rotate_angle
        self.angle += self.rotate_angle
        print('The robot turned to', self.angle, 'degrees.')
    
    def stop(self):
        print('The robot stopped.')

Robot1 = Robot(0,0,5,0)
Robot1.forward(10)
Robot1.rotate(45)
Robot1.forward(10)
Robot1.stop()

