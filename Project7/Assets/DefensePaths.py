import math, random
from panda3d.core import *

def Cloud(radius = 1):
    x = 2 * random.random() - 1
    y = 2 * random.random() - 1
    z = 2 * random.random() - 1

    unitVec = Vec3(x, y, z)
    unitVec.normalize()

    return unitVec * radius

def BaseballSeams(step, numSeams, B, F = 1):
    time = step / float(numSeams) * 2 * math.pi

    F4 = 0

    R = 1

    xxx = math.cos(time) - B * math.cos(3 * time)
    yyy = math.sin(time) + B * math.sin(3 * time)
    zzz = F * math.cos(2 * time) + F4 * math.cos(4 * time)

    rrr = math.sqrt(xxx ** 2 + yyy ** 2 + zzz ** 2)

    x = R * xxx / rrr
    y = R * yyy / rrr
    z = R * zzz / rrr

    return Vec3(x, y, z)

def CircleX(radius = 1, numPoints = 100):
    points = []
    for i in range(numPoints):
        angle = 2 * math.pi * i / numPoints
        x = 0
        y = radius * math.cos(angle)
        z = radius * math.sin(angle)
        points.append(Vec3(x, y, z))
    return points

def CircleY(radius = 1, numPoints = 100):
    points = []
    for i in range(numPoints):
        angle = 2 * math.pi * i / numPoints
        x = radius * math.cos(angle)
        y = 0
        z = radius * math.sin(angle)
        points.append(Vec3(x, y, z))
    return points

def CircleZ(radius = 1, numPoints = 100):
    points = []
    for i in range(numPoints):
        angle = 2 * math.pi * i / numPoints
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        z = 0
        points.append(Vec3(x, y, z))
    return points