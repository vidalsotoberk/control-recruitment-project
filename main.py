import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
import math # for pure pursuit?
from simulator import Simulator, centerline

sim = Simulator()

def reverse_centerline(x, y):
    """
    takes in some x and y coordinate and returns the closest centerline position
    """



def controller(x):
    """controller for a car

    Args:
        x (ndarray): numpy array of shape (5,) containing [x, y, heading, velocity, steering angle]

    Returns:
        ndarray: numpy array of shape (2,) containing [fwd acceleration, steering rate]
    """
    xpos   = x[0]                   # current x position
    ypos   = x[1]                   # current y position
    phi    = np.mod(x[2], 2*np.pi)  # current heading (radians) (direction of car?)
    v      = x[3]                   # current velocity
    theta   = x[4]                  # current steering angle

    ... # YOUR CODE HERE
    """
    BIG IDEA: need to check where the car is and how fast it going, and then determine
    how the car should accelerate and how much to turn the steering wheel

    Notes:
    -- using current state --> we need use the centerline and heading of the car to determine
    the error and where we want to go on the centerline to create some derivative
    -- Jaden hint: do centerline on the whole length (0-105) and use all the x and y coords
    with cubic spline to separate functions? kinda
    -- need to make a function that takes in a x and y coordinate and returns the closest centerline position from 0 to 105

    """
    centerline_x = []
    centerline_y = []

    for i in range(0, 105):
        xy_coord = []
        xy_coord.append(centerline(i))
        
        centerline_x.append(xy_coord[0])
        centerline_y.append(xy_coord[1])

    cs = CubicSpline(centerline_x, centerline_y)
    

    """
    we are going to return two things:
    a - how much should the car accelerate or deccelerate
    theta - turning left or right
    """
    return np.array([0,0])




sim.set_controller(controller)
sim.run()
sim.animate()
sim.plot()