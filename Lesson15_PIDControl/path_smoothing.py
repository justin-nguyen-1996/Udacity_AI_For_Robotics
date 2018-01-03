# temp.py
# -----------
# User Instructions
#
# Define a function smooth that takes a path as its input
# (with optional parameters for weight_data, weight_smooth,
# and tolerance) and returns a smooth path. The first and
# last points should remain unchanged.
#
# Smoothing should be implemented by iteratively updating
# each entry in newpath until some desired level of accuracy
# is reached. The update should be done according to the
# gradient descent equations given in the instructor's note
# below (the equations given in the video are not quite
# correct).
# -----------

from copy import deepcopy
import numpy as np

# thank you to EnTerr for posting this on our discussion forum
def printpaths(path,newpath):
    for old,new in zip(path,newpath):
        print '['+ ', '.join('%.3f'%x for x in old) + \
               '] -> ['+ ', '.join('%.3f'%x for x in new) +']'

# Don't modify path inside your function.
path = [[0, 0],
        [0, 1],
        [0, 2],
        [1, 2],
        [2, 2],
        [3, 2],
        [4, 2],
        [4, 3],
        [4, 4]]

# yi <- yi + alpha (xi - yi) + beta (y_i+1 + y_i-1 - 2 * yi)
def smooth(path, weight_data = 0.5, weight_smooth = 0.1, tolerance = 0.000001):

    # Make a deep copy of path into newpath
    path = np.array(path).astype(float)
    newpath = np.array(deepcopy(path)).astype(float)

    total_change = tolerance
    while total_change >= tolerance:
        total_change = 0.0
        for i in range(1, len(path)-1):
            xi = path[i]
            yi = newpath[i]
            aux = np.copy(newpath[i])
            yi_p1 = newpath[i+1]
            yi_m1 = newpath[i-1]
            newpath[i] += weight_data * (xi - yi) + weight_smooth * (yi_p1 + yi_m1 - 2.0*yi)
            total_change += abs(aux[0] - yi[0]) + abs(aux[1] - yi[1])

    return newpath # Leave this line for the grader!

printpaths(path,smooth(path))
# -----------
