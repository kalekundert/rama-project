import vector
import math

for i in range(12):
    x = math.cos(2 * math.pi * i / 12)
    y = math.sin(2 * math.pi * i / 12)

    v1 = [-1, 0, 0]
    v2 = [0, 0, 0]
    v3 = [x, y, 0]

    print v3
    print vector.angle(v1, v2, v3)
    print

