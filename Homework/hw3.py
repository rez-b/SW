import numpy as np
import matplotlib.pyplot as plt

class Simulation:
    def __init__(self, Vx0, Vy0, T, g=9.8):
        self.g = g
        self.Vx0 = Vx0
        self.Vy0 = Vy0
        self.T = T

    def simulate(self):
        self.t = np.arange(0, self.T+1)
        self.Vx = self.Vx0 - self.g * self.t
        self.Vy = self.Vy0 + self.t*0
        self.x = self.Vx0 * self.t - 0.5*self.g*self.t*self.t
        self.y = self.Vy0 * self.t

    def save_to_txt(self):
        with open('output.txt', 'w') as file:
            file.write(f"Time: {self.t}\n")
            file.write(f"X: {self.x}\n")
            file.write(f"Y: {self.y}\n")
            file.write(f"Vx: {self.Vx}\n")
            file.write(f"Vy: {self.Vy}\n")
    

if __name__ == '__main__':
    Vx0 = int(input("Enter the horizontal velocity (Vx): "))
    Vy0 = int(input("Enter the vertical velocity (Vy): "))
    T = int(input("Enter the total time (T): "))

    sim = Simulation(Vx0, Vy0, T)

    sim.simulate()
    sim.save_to_txt()
 