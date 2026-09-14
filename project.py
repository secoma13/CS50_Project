import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

class Pendulum:
    def __init__(self, m : float, l : float, theta : float):
        self.mass = m
        self.length = l
        self.angle = theta

    def __str__(self):
        print("This is a pendulum whose mass is {self.mass} kg, and whose length is {slef.length} m.")

    # We define mass as a property to ensure that it is a positive float
    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, m):
        if m <= 0:
            raise ValueError("Length should be a positive number")
        else:
            self._mass = m

    # We do the same fot the length
    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, l):
        if l <= 0:
            raise ValueError("Length should be a positive number")
        else:
            self._length = l

        
def get_mass_lengths():
    """
    Gets the masses and lengths of the pendulum. Index one refers to the pendulum that hangs from the ceiling.

    
    """

    print("Introduce the date required to describe the system.")
    m1 : float = input("Mass of the first pendulum in kgs: ")
    m2 : float = input("Mass of the second pendulum in kgs: ")
    l1 : float = input("Length of the rope between the ceiling and the first pendulum in meters: ")
    l2 : float = input("Length of the rope between the pendulum in meters")

    return (m1, m2, l1, l2)

def get_init_cond():
    """
    Gets the initial conditions of the pendulum
    """

    print("Intorduce the initial conditions for the pendulum. \n Recall that these are given by two angles (that are expected in degrees)")
    theta1 : float = input("Introduce the angle of the first pendulum: ")
    theta2 : float = input("Introduce the angle of the second pendulum: ")

    return theta1, theta2


def radians(theta :  float) -> float:
    """
    Converts an angle in degrees to radians 
    """
    return theta*2*math.py/180

def main():
    GRAVITY = 9.8

    # Input of the system
    m1, m2, l1, l2 = get_mass_lengths()

    # Initial conditions
    theta1, theta2 = get_init_cond()

    # Create the pendulums
    p1 = Pendulum(m1, l1, theta1)
    p2 = Pendulum(m2, l2, theta2)

if __name__ == "__main__":
    main()