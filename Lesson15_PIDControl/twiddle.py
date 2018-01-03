# pid_controller.py
# -----------
# User Instructions
#
# Implement a P controller by running 100 iterations
# of robot motion. The steering angle should be set
# by the parameter tau so that:
#
# steering = -tau_p * CTE - tau_d * diff_CTE - tau_i * int_CTE
#
# where the integrated crosstrack error (int_CTE) is
# the sum of all the previous crosstrack errors.
# This term works to cancel out steering drift.
#
# Your code should print a list that looks just like
# the list shown in the video.
#
# Only modify code at the bottom!
# ------------

import random
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------
#
# this is the Robot class
#

class Robot(object):
    def __init__(self, length=20.0):
        """
        Creates robot and initializes location/orientation to 0, 0, 0.
        """
        self.x = 0.0
        self.y = 0.0
        self.orientation = 0.0
        self.length = length
        self.steering_noise = 0.0
        self.distance_noise = 0.0
        self.steering_drift = 0.0

    def set(self, x, y, orientation):
        """
        Sets a robot coordinate.
        """
        self.x = x
        self.y = y
        self.orientation = orientation % (2.0 * np.pi)

    def set_noise(self, steering_noise, distance_noise):
        """
        Sets the noise parameters.
        """
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.steering_noise = steering_noise
        self.distance_noise = distance_noise

    def set_steering_drift(self, drift):
        """
        Sets the systematical steering drift parameter
        """
        self.steering_drift = drift

    def move(self, steering, distance, tolerance=0.001, max_steering_angle=np.pi / 4.0):
        """
        steering = front wheel steering angle, limited by max_steering_angle
        distance = total distance driven, most be non-negative
        """
        if steering > max_steering_angle:
            steering = max_steering_angle
        if steering < -max_steering_angle:
            steering = -max_steering_angle
        if distance < 0.0:
            distance = 0.0

        # make a new copy
        # res = Robot()
        # res.length = self.length
        # res.steering_noise = self.steering_noise
        # res.distance_noise = self.distance_noise
        # res.steering_drift = self.steering_drift

        # apply noise
        steering2 = random.gauss(steering, self.steering_noise)
        distance2 = random.gauss(distance, self.distance_noise)

        # apply steering drift
        steering2 += self.steering_drift

        # Execute motion
        turn = np.tan(steering2) * distance2 / self.length

        if abs(turn) < tolerance:
            # approximate by straight line motion
            self.x += distance2 * np.cos(self.orientation)
            self.y += distance2 * np.sin(self.orientation)
            self.orientation = (self.orientation + turn) % (2.0 * np.pi)
        else:
            # approximate bicycle model for motion
            radius = distance2 / turn
            cx = self.x - (np.sin(self.orientation) * radius)
            cy = self.y + (np.cos(self.orientation) * radius)
            self.orientation = (self.orientation + turn) % (2.0 * np.pi)
            self.x = cx + (np.sin(self.orientation) * radius)
            self.y = cy - (np.cos(self.orientation) * radius)

    def __repr__(self):
        return '[x=%.5f y=%.5f orient=%.5f]' % (self.x, self.y, self.orientation)

############## ADD / MODIFY CODE BELOW ####################
# ------------------------------------------------------------------------
#
# run - does a single control run

def make_robot():
    """
    Resets the robot back to the initial position and drift.
    You'll want to call this after you call `run`.
    """
    robot = Robot()
    robot.set(0, 1, 0)
    robot.set_steering_drift(10 / 180 * np.pi)
    return robot

# steering = -tau_p * CTE - tau_d * diff_CTE - tau_i * int_CTE
def run(robot, params, n=100, speed=1.0):
    x_trajectory = []
    y_trajectory = []
    prev_CTE = robot.y
    int_CTE = 0
    tau_p = params[0]
    tau_d = params[1]
    tau_i = params[2]
    err = 0
    for i in range(2 * n):
        CTE = robot.y
        diff_CTE = robot.y - prev_CTE
        prev_CTE = CTE
        int_CTE += CTE
        steering = -tau_p*CTE - tau_d*diff_CTE - tau_i*int_CTE
        robot.move( steering, speed )
        x_trajectory.append( robot.x )
        y_trajectory.append( robot.y )
        if i >= n:
            err += CTE ** 2
    return x_trajectory, y_trajectory, err/n

def twiddle(tolerance = 0.001):
    p  = [0.0 , 0.0 , 0.0]
    dp = [1.0 , 1.0 , 1.0]
    robot = make_robot()
    x_trajectory, y_trajectory, best_error = run(robot, p)
    it = 0
    while sum(dp) > tolerance:
        print("Iteration {}, best error = {}".format(it, best_error))
        for i in range(len(p)):

            p[i] += dp[i]
            robot = make_robot()
            x_trajectory, y_trajectory, error = run(robot, p)
            if error < best_error:
                best_error = error
                dp[i] *= 1.1
                continue

            p[i] -= 2.0 * dp[i]
            robot = make_robot()
            x_trajectory, y_trajectory, error = run(robot, p)
            if error < best_error:
                best_error = error
                dp[i] *= 1.1
                continue

            p[i] += dp[i]
            dp[i] *= 0.9
        it += 1
    return p

params = twiddle()
robot = make_robot()
x_trajectory, y_trajectory, err = run(robot, params)
n = len(x_trajectory)
print err
print params

plt.plot(x_trajectory, y_trajectory, 'g', label='PID controller')
plt.plot(x_trajectory, np.zeros(n), 'r', label='reference')
plt.legend()
plt.show()
