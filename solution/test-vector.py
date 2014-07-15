#!/usr/bin/env python2

import vector
import math

v1 = [36.886, 53.177, 21.887]
v2 = [38.323, 52.817, 21.996]
v3 = [38.493, 51.553, 22.830]
v4 = [39.483, 50.748, 22.463]

n1 = vector.normalize(v1)
n2 = vector.normalize(v2)

v1 = n1 = 1,2,3
v2 = n2 = 3,4,5

print vector.add(v1, v2)
print vector.subtract(v1, v2)
print vector.normalize(v1)
print vector.dot(n1, n2)
print vector.cross(n1, n2)
print vector.torsion(v1, v2, v3, v4)
