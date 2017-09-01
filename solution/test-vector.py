#!/usr/bin/env python2

import vector
import math

v1 = 1,2,3
v2 = 3,4,5
n1 = vector.normalize(v1)

assert vector.add(v1, v2) == (4, 6, 8)
assert vector.subtract(v1, v2) == (-2, -2, -2)
assert abs(n1[0] - 0.27) < 0.01 and \
       abs(n1[1] - 0.53) < 0.01 and \
       abs(n1[2] - 0.80) < 0.01
assert vector.dot(v1, v2) == 26
assert vector.cross(v1, v2) == (-2, 4, -2)

print "All tests passed!"
