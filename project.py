import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
from scipy.integrate import solve_ivp

class Pendulum:
    def __init__(self, m : float, l : float, theta : float, speed : float):
        self.mass = m
        self.length = l
        self.angle = theta
        self.speed = speed

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
    Gets the masses and lengths of the pendulum. Index one refers to the pendulum that hangs from the ceiling, and index two to the one hanging from the first one.

    :return: Mass and length of the system
    :rtype: tuple 
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

    :return: Initial conditions of the pendulum
    :rtype: tuple
    """

    print("Intorduce the initial conditions for the pendulum. \n Recall that these are given by two angles (that are expected in degrees)")
    theta1 : float = input("Introduce the angle of the first pendulum: ")
    theta2 : float = input("Introduce the angle of the second pendulum: ")
    theta1_dot : float = input("Introduce the initial speed of the first pendulum (degrees per second): ")
    theta2_dot : float = input("Introduce the initial speed of the second pendulum (degrees per second): ")
    return theta1, theta2, theta1_dot, theta2_dot

def ode_fun(t, y, m1, m2, l1, l2):
    g = 9.8

    # ODE
    denom = l1*(2*m1 + m2*(1 - math.cos(2*(y[0]-y[1]))))

    dot_y2 = 1/denom*(-g(*(2*m1 + m2)*math.sin(y[0]) - m2*math.sin(y[0]-2*y[1])) - 2*m2*math.sin(y[0] - y[1])*((y[3]**2)*l2 + (y[2]**2)*l1*math.cos(y[0] - y[1])))
    dot_y3 = 1/denom*(2*math.sin(y[0] - y[1])*((y[2]**2)*l1*(m1 + m2) + g*(m1 + m2)*math.cos(y[0]) + (y[3]**2)*l2*m2*math.cos(y[0] - y[1])))

    return [y[2], y[3], dot_y2, dot_y3]

def radians(theta :  float) -> float:
    """
    Converts an angle in degrees to radians 
    """
    return theta*2*math.py/180

def coordinate_transf(l1 : float, l2 : float, theta1 : float, theta2 : float):
    """
    Transforms spherical coordinates to cartesian coordinates
    
    
    Parameters
    ----------
    l1, l2: float
        Legths of the double pendulum
    theta1, theta2: float
        Positions of the pendulum

    Returns
    -------
    float
        Cartesian coordiantes of the masses
    """
    x1 = l1*math.cos(theta1)
    y1 = -l1*math.sin(theta1)

    return (x1, y1, x1 + l2*math.cos(theta2), y1 - l2*math.sin(theta2))



def main():

    # Input of the system
    m1, m2, l1, l2 = get_mass_lengths()

    # Initial conditions
    theta1, theta2, theta1_dot, theta2_dot = get_init_cond()

    # Create the pendulums
    p1 = Pendulum(m1, l1, radians(theta1), radians(theta1_dot))
    p2 = Pendulum(m2, l2, radians(theta2), radians(theta2_dot))

    # Solve the IVP (Initial Value Problem)
    # sol is an object. sol.t is the time points at which we get the solutions and sol.y are the solutions (it is an np.array)
    # y0 is the angle of the first pendulum, y1 of the second, and y2 and y3 are theire respective velocites.
    # For the plot only the positions matter
    sol = solve_ivp(fun = ode_fun, t_span = (0, 30), t_eval = np.linspace(0, 30, 1000), y0 = [theta1, theta2, theta1_dot, theta2_dot], args = (m1, m2, l1, l2))

    # Plot the solution
    # We fix a coordinate system where (0,0) is the point where the rope l1 touches the ceiling

    for i in range(0:1000):
        x1_t, y1_t, x2_t, y2_t = coordinate_transf(l1, l2, sol.y[0, i], sol.y[1, i])
        pass



if __name__ == "__main__":
    main()
