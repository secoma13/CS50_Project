import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter
import math
from scipy.integrate import solve_ivp
import random as rd

def get_mass_lengths():
    """
    Gets the masses and lengths of the pendulum. Index one refers to the pendulum that hangs from the ceiling, and index two to the one hanging from the first one.

    :return: Mass and length of the system
    :rtype: tuple 
    """

    print("Introduce the date required to describe the system.")
    m1 : float = float(input("Mass of the first pendulum in kgs: "))
    m2 : float = float(input("Mass of the second pendulum in kgs: "))
    l1 : float = float(input("Length of the rope between the ceiling and the first pendulum in meters: "))
    l2 : float = float(input("Length of the rope between the pendulum in meters: "))

    return (m1, m2, l1, l2)

def get_init_cond():
    """
    Gets the initial conditions of the pendulum

    :return: Initial conditions of the pendulum
    :rtype: tuple
    """

    print("Intorduce the initial conditions for the pendulum. \nRecall that these are given by two angles (that are expected in degrees)")
    theta1 : float = float(input("Introduce the angle of the first pendulum: "))
    theta2 : float = float(input("Introduce the angle of the second pendulum: "))
    theta1_dot : float = float(input("Introduce the initial speed of the first pendulum (degrees per second): "))
    theta2_dot : float = float(input("Introduce the initial speed of the second pendulum (degrees per second): "))
    return theta1, theta2, theta1_dot, theta2_dot

def ode_fun(t, y, m1, m2, l1, l2):
    g = 9.8

    # ODE
    denom = 2*m1 + m2*(1 - math.cos(2*(y[0]-y[1])))

    dot_y2 = 1/(l1*denom)*(-g*((2*m1 + m2)*math.sin(y[0]) + m2*math.sin(y[0]-2*y[1])) - 2*m2*math.sin(y[0] - y[1])*((y[3]**2)*l2 + (y[2]**2)*l1*math.cos(y[0] - y[1])))
    dot_y3 = 1/(l2*denom)*(2*math.sin(y[0] - y[1])*((y[2]**2)*l1*(m1 + m2) + g*(m1 + m2)*math.cos(y[0]) + (y[3]**2)*l2*m2*math.cos(y[0] - y[1])))

    return [y[2], y[3], dot_y2, dot_y3]

def radians(theta : float) -> float:
    """
    Converts an angle in degrees to radians 
    """
    return theta*math.pi/180

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
    x1 = l1*math.sin(theta1)
    y1 = -l1*math.cos(theta1)

    return (x1, y1, x1 + l2*math.sin(theta2), y1 - l2*math.cos(theta2))


def kin_en(theta1 : float, theta2 : float, theta1_dot : float, theta2_dot : float, l1 : float, l2 : float, m1 : float, m2 : float) -> float:
    """
    Calculates the kinetic energy of a pendulum

    Parameters
    ----------
    theta1, theta2: float
        Angles of the pendulums
    theta1_dot, theta2_dot: float
        Angular velocities of the pendulums
    l1, l2: float
        lengths of the rods
    m1, m2: float
        masses of the pendulums
    
    Return
    --------
    float:
        Kinetic energy of the system
    
    """
    return 0.5*((m1 + m2)*(l1*theta1_dot)**2 + m2*(l2*theta2_dot)**2) + m2*l1*l2*theta1_dot*theta2_dot*math.cos(theta1-theta2)


def pot_en(h : float, m : float) -> float:
    """
    Calculates the potential energy of a pendulum

    Parameters
    ----------
    h: float
        height of the pendulum
    m: float
        mass of the pendulum

    Returns
    --------
        float
            Potential energy of ONE mass at height h
    """
    return m*h*9.8


def main():

    # Input of the system
    m1, m2, l1, l2 = get_mass_lengths()

    # Initial conditions
    theta1, theta2, theta1_dot, theta2_dot = get_init_cond()
    print(theta1)

    # Transform angles and ang. velocities to radians 
    theta1 = radians(theta1)
    theta2 = radians(theta2)
    theta1_dot = radians(theta1_dot)
    theta2_dot = radians(theta2_dot)

    # Perturbed pendulum (we will modify the initial of each pendulum position by 0.05 degrees)
    # We keep the initial velocities the same
    epsilon = radians(0.5)
    rd_list = [-1, 1]

    theta1_p2 = theta1 + rd.choice(rd_list)*epsilon
    theta2_p2 = theta2 + rd.choice(rd_list)*epsilon

    # Solve the IVP (Initial Value Problem)
    # sol is an object. sol.t is the time points at which we get the solutions and sol.y are the solutions (it is an np.array)
    # y0 is the angle of the first pendulum, y1 of the second, and y2 and y3 are theire respective velocites.
    # For the plot only the positions matter

    sol1 = solve_ivp(fun = ode_fun, t_span = (0, 50), t_eval = np.linspace(0, 50, 1200), y0 = [theta1, theta2, theta1_dot, theta2_dot], args = (m1, m2, l1, l2))

    sol2 = solve_ivp(fun = ode_fun, t_span = (0, 50), t_eval = np.linspace(0, 50, 1200), y0 = [theta1_p2, theta2_p2, theta1_dot, theta2_dot], args = (m1, m2, l1, l2))

    # Plot the solution
    # We fix a coordinate system where (0,0) is the point where the rope l1 touches the ceiling
    # We create the figures. We plot both the animation displaying both pendulums and the evolution of the kinetic and potential energies over time
    fig, axs = plt.subplots(nrows = 1, ncols = 2, figsize = (14, 6), width_ratios = (1, 1))
    fig.suptitle("Double Pendulum")
    pends = axs[0]
    energ = axs[1]
    pends.set_title("Simulated movement")
    energ.set_title("Energy distribution")

    # Data to plot the pendulums
    # Pendulum1
    M = m1 + m2
    sizes = [100*m1/M, 100*m2/M]
    pendulum1_rod, = pends.plot([], [], color = "blue", linestyle = "-")
    pendulum1_mass = pends.scatter([0, 0], [0, 0], color ="blue", marker = 'o', s = sizes)

    # Pendulum 2
    pendulum2_rod, = pends.plot([], [], color = "orange", linestyle = "-")
    pendulum2_mass = pends.scatter([0 ,0], [0, 0], color = "orange", marker = "o", s = sizes) 

    # To set the axis limit we calculate the initial mecanical energy
    _, y1, __, y2 = coordinate_transf(l1, l2, theta1, theta2)
    E = kin_en(theta1, theta2, theta1_dot, theta2_dot, l1, l2, m1, m2) + pot_en(y2, m2) + pot_en(y1, m1)
    energ.set_ylim(-E, 3*E)

    categ = ["Kinetic", "Potential", "Total"]
    energ_plot = energ.bar(x = categ, height = [0, 0, E], color = ["red", "green", "blue"])

    # We set the axis (we add the 1.5 to see both pendulums at every point)
    l12 = l1 + l2 + 1.5
    pends.set_xlim(-l12, l12)
    pends.set_ylim(-l12, l12)

    # We create the animation
    metadata = dict(title = "Double Pendulum", artist = "Sergio Martín Nieto")
    writer = PillowWriter(fps = 24, metadata = metadata)

    # The with writer.saving is similar to the synthax we use to open/close files
    with writer.saving(fig, "DoublePendulum.gif", 75):
        for i in range(1200):
            x1_t, y1_t, x2_t, y2_t = coordinate_transf(l1, l2, sol1.y[0, i], sol1.y[1, i])
            x1_t_p2, y1_t_p2, x2_t_p2, y2_t_p2 = coordinate_transf(l1, l2, sol2.y[0, i], sol2.y[1, i])

            # Set first pendulum
            pendulum1_rod.set_data([0, x1_t, x2_t], [0, y1_t, y2_t])
            pendulum1_mass.set_offsets([[x1_t, y1_t], [x2_t, y2_t]])

            # Set second pendulum
            pendulum2_rod.set_data([0, x1_t_p2, x2_t_p2], [0, y1_t_p2, y2_t_p2])
            pendulum2_mass.set_offsets([[x1_t_p2, y1_t_p2], [x2_t_p2, y2_t_p2]])

            # Set data for the energies
            K = kin_en(sol1.y[0, i], sol1.y[1, i], sol1.y[2, i], sol1.y[3, i], l1, l2, m1, m2)
            V = pot_en(y1_t, m1) + pot_en(y2_t, m2)
            energ_plot[0].set_height(K)
            energ_plot[1].set_height(V)
            energ_plot[2].set_height(K + V)

            # We get the frame
            writer.grab_frame()


if __name__ == "__main__":
    main()
