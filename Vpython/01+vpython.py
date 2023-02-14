#!/usr/bin/env python3
from vpython import *
from time import *
import numpy as np
import math

scene.range = 5
scene.forward = vector(-1, -.5, -1)
scene.width = 600
scene.height = 600
toRad = 2*np.pi/360
toDeg = 1/toRad

xarrow = arrow(length=2, shaftwidth=.1, color=color.red, axis=vector(1, 0, 0))
yarrow = arrow(length=2, shaftwidth=.1, color=color.green, axis=vector(0, 1, 0))
zarrow = arrow(length=2, shaftwidth=.1, color=color.blue, axis=vector(0, 0, 1))

lengthAxis = arrow(length=4, shaftwidth=.1, color=color.purple, axis=vector(1, 0, 0))
querAxis = arrow(length=4, shaftwidth=.1, color=color.orange, axis=vector(0, 0, 1))
verticalAxis = arrow(length=4, shaftwidth=.1, color=color.magenta, axis=vector(0, 1, 0))

board = box(length=6, width=2, height=.2, opacity=.8, pos=vector(0, 0, 0))
head = triangle

while (True):
    pitch=30*toRad
    for yaw in np.arange(0, 2*np.pi, .01):
        rate(50)
        lengthVector=vector(cos(yaw)*cos(pitch), sin(pitch), sin(yaw)*cos(pitch))
        yAxis = vector(0, 1, 0)
        querVector = cross(lengthVector, yAxis) # it is a cross product !!
        verticalVector = cross(querVector, lengthVector)

        lengthAxis.axis = lengthVector
        querAxis.axis = querVector
        verticalAxis.axis = verticalVector
        board.axis=lengthVector
        board.up=verticalVector
        board.length=6
        lengthAxis.length = 4
        querAxis.length = 3
        verticalAxis.length = 3



box_location = vector(0,0, 0)

#box(pos=box_location, size=vector(5, 0.3,2), color=color.red) # size = width, height, depth