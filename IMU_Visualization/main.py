from vpython import *

import math
import serial
import struct


scene.range = 5
scene.forward = vector(-1, -.5, -1)
scene.width = 600
scene.height = 600

xarrow = arrow(length=2, shaftwidth=.1, color=color.red, axis=vector(1, 0, 0))
yarrow = arrow(length=2, shaftwidth=.1, color=color.green, axis=vector(0, 1, 0))
zarrow = arrow(length=2, shaftwidth=.1, color=color.blue, axis=vector(0, 0, 1))

lengthAxis = arrow(length=4, shaftwidth=.1, color=color.purple, axis=vector(1, 0, 0))
querAxis = arrow(length=4, shaftwidth=.1, color=color.orange, axis=vector(0, 0, 1))
verticalAxis = arrow(length=4, shaftwidth=.1, color=color.magenta, axis=vector(0, 1, 0))

board = box(length=6, width=2, height=.2, opacity=.8, pos=vector(0, 0, 0))

while True:

    # Read the 4 quaternion elements one byte at a time
        ser = serial.Serial("/dev/ttyUSB0", 9600)  # replace with your serial port name and baud rate

        # Read the 4 quaternion elements
        qw, qx, qy, qz = struct.unpack("<dddd", ser.read(32))

        roll = math.atan2(2 * (qw * qx + qy * qz), 1 - 2 * (qx * qx + qy * qy))
        yaw = math.atan2(2 * (qw * qz + qx * qy), 1 - 2 * (qy * qy + qz * qz))
        pitch = math.asin(-math.cos(roll) * math.sin(yaw))

        print(format(qw, '.3f'), format(qx, ' .3f'), format(qy, ' .3f'), format(qz, ' .3f'))
        # print(format(roll, '.3f'), format(yaw, ' .3f'), format(pitch, ' .3f'))

        rate(50)
        lengthVector = vector(cos(yaw) * cos(pitch), sin(pitch), sin(yaw) * cos(pitch))
        yAxis = vector(0, 1, 0)
        querVector = cross(lengthVector, yAxis)  # it is a cross product !!
        verticalVector = cross(querVector, lengthVector)
        verticalVectorRot = verticalVector * cos(roll) + cross(lengthVector, verticalVector) * sin(roll)

        lengthAxis.axis = lengthVector
        querAxis.axis = cross(lengthVector, verticalVectorRot)
        verticalAxis.axis = verticalVectorRot
        board.axis = lengthVector
        board.up = verticalVectorRot
        board.length = 6
        lengthAxis.length = 4
        querAxis.length = 3
        verticalAxis.length = 3

        ser.close()
