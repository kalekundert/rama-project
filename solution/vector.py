from __future__ import division

import math

def add(v1, v2):
    return v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]

def subtract(v1, v2):
    return v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2]

def multiply(v, k):
    return k * v1[0], k * v1[1], k * v1[2]

def divide(v, k):
    return v[0] / k, v[1] / k, v[2] / k


def magnitude(v):
    return math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)

def normalize(v):
    return divide(v, magnitude(v))

def dot(v1, v2):
    return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]

def cross(v1, v2):
    return (v1[1]*v2[2] - v1[2]*v2[1],
            v1[2]*v2[0] - v1[0]*v2[2],
            v1[0]*v2[1] - v1[1]*v2[0])


def length(v1, v2):
    return magnitude(subtract(v2, v1))

def angle(v1, v2, v3):
    r1 = subtract(v1, v2)
    r2 = subtract(v3, v2)

    r1 = normalize(r1)
    r2 = normalize(r2)

    cosine = dot(r1, r2)
    radians = math.acos(cosine)
    return math.degrees(radians)

def torsion(v1, v2, v3, v4):
    r1 = subtract(v1, v2)
    r2 = subtract(v2, v3)
    r3 = subtract(v3, v4)

    r1 = normalize(r1)
    r2 = normalize(r2)
    r3 = normalize(r3)

    n1 = cross(r1, r2)
    n2 = cross(r2, r3)

    x = dot(n1, n2)
    y = dot(cross(n1, r2), n2)

    radians = math.atan2(y, x)
    return math.degrees(radians)

