import numpy as np
import matplotlib.pyplot as plt # unneeded i think
from scipy.interpolate import CubicSpline
import math
from simulator import Simulator, centerline

sim = Simulator()

centerline_x = []
centerline_y = []
s_values = []

for i in np.arange(0, 105, 0.5):
    s_values.append(i)  # fills s_values with values from 0-104.5 in intervals of 0.5

for s in s_values:  # gets the pairs of x and y coords for each centerline(s) and separates them
    xy_coord = []
    xy_coord.append(centerline(s))
    centerline_x.append(xy_coord[0][0])
    centerline_y.append(xy_coord[0][1])

spline_x = CubicSpline(s_values, centerline_x)
spline_y = CubicSpline(s_values, centerline_y)
spline_x_derivative = spline_x.derivative() # these derivatives will help me know what way the track is pointin
spline_y_derivative = spline_y.derivative()
    

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
    """
    # lines 49 - 59
    nearest = reverse_centerline(xpos, ypos)    # takes the current x and y positions and finds where on the centerline it is

    der_x_evaluation = spline_x_derivative(nearest)   
    der_y_evaluation = spline_y_derivative(nearest)

    track_heading = math.atan2(der_y_evaluation, der_x_evaluation)  # atan2 gives me the heading angle 

    heading_error = track_heading - phi
    heading_error = np.mod((heading_error + np.pi), 2*np.pi) - np.pi


    # lines 62 - 67 take car of controlling speed
    target_velocity = 5
    speed_error = target_velocity - v       # positive error = more accel, negative error = less accel/brake
    speed_gain = 1

    requested_accel = speed_gain * speed_error
    bounded_accel = np.clip(requested_accel, -10, 4)    #np.clip takes care of the bounds for me

    # lines 78 - 95 take care of telling how far the car is from the centerline and how the car should steer to get closer to it
    ref_point_x = spline_x(nearest) # ref coords for nearest centerline - WHERE I WANT TO GO
    ref_point_y = spline_y(nearest) # same thing but y

    delta_x = ref_point_x - xpos    # displacement for x -- how far the car is from the actual centerline
    delta_y = ref_point_y - ypos    #displacement for y -- same thing

    centerline_tracking_error = (-delta_x * np.sin(track_heading) + delta_y * np.cos(track_heading))    # gets the lateral error of the car

    heading_gain = 1
    centerline_tracking_gain = 0.1
    steering_gain = 4

    requested_theta = (heading_gain * heading_error + centerline_tracking_gain * centerline_tracking_error) #i combine heading correction and lateral correction to get the desired wheel angle
    bounded_theta = np.clip(requested_theta, -0.7, 0.7) # bounded

    theta_error = bounded_theta - theta # compares desired wheel angle with actual wheel angle
    requested_steering_rate = steering_gain * theta_error   
    bounded_steering_rate = np.clip(requested_steering_rate, -1, 1) # bounded
    """
    we are going to return two things:
    a - how much should the car accelerate or deccelerate
    steering rate - turning left or right and how fast
    """
    return np.array([bounded_accel, bounded_steering_rate])

def reverse_centerline(x, y):
    """takes in some x and y coordinate and returns the closest centerline position"""

    shortest_distance = np.inf #infinity so anything will beat it at first
    for i in range(0 , len(s_values)):
        corresponding_x = centerline_x[i]
        corresponding_y = centerline_y[i]
        distance = (corresponding_x - x)**2 + (corresponding_y - y)**2
        if distance < shortest_distance:
            shortest_distance = distance
            best_index = i
    
    return s_values[best_index]

sim.set_controller(controller)
sim.run()
sim.animate()
sim.plot()