# temp.py

import numpy as np
a = [[[x] for x in range(4)] for y in range(3)]
print np.array(a)
row = a[0][0]
row.append(-1)
print np.array(a)
print "pop: ", row.pop()
print "pop: ", row.pop()
print "pop: ", row.pop()
print np.array(a)
