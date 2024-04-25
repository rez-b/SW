#Variant 3
from math import *
class Robot:
    def __init__(self, x, y, velocity, angle):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.angle = angle

    def Forward(self, TimeInSeconds):
        self.TimeInSeconds = TimeInSeconds
        self.x += self.velocity*TimeInSeconds*cos(self.angle*pi/180)
        self.y += self.velocity*TimeInSeconds*sin(self.angle*pi/180)
        print('Coordinates of the robot:', self.x, self.y)
    def Rotate(self, RotateAngle):
        self.RotateAngle = RotateAngle
        self.angle += self.RotateAngle
        print('The robot turned to', self.angle, 'degrees.')
    
    def Stop(self):
        print('The robot stopped.')

Robot1 = Robot(0,0,5,0)
Robot1.Forward(10)
Robot1.Rotate(45)
Robot1.Forward(10)
Robot1.Stop()
