#!/usr/bin/env python3
import time
import numpy as np
import serial
import struct
import math

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    rollOld = 0.0
    pitchOld = 0.0
    yawOld = 0.0
    toRad = 2 * np.pi / 360
    toDeg = 1 / toRad
    s = serial.Serial("/dev/ttyUSB2", 9600)
    buff = b''
    oldTime = time.time()
    while s.read() != b'\n':
        pass
    while True:
        c = s.read()

        if c == b'\n':
            newTime = time.time()
            dt = newTime - oldTime
            raw = struct.unpack(">2H7h2H", buff)
            oldTime = newTime
            rollMesured = (raw[2]) * dt
            pitchMesured = (raw[3] ) * dt
            yawMesured = (raw[4]) * dt


            # Quaternions from roll, pitch and yaw
            c_pitch = math.cos((pitchMesured * toRad) / 2)
            c_yaw = math.cos((yawMesured * toRad) / 2)
            c_roll = math.cos((rollMesured * toRad) / 2)

            s_pitch = math.sin((pitchMesured * toRad) / 2)
            s_yaw = math.sin((yawMesured * toRad) / 2)
            s_roll = math.sin((rollMesured * toRad) / 2)

            qw = c_roll * c_pitch * c_yaw + s_roll * s_pitch * s_yaw
            qx = s_roll * c_pitch * c_yaw - c_roll * s_pitch * s_yaw
            qy = c_roll * s_pitch * c_yaw + c_pitch * s_yaw * s_roll
            qz = c_roll * c_pitch * s_yaw + s_roll * s_pitch * c_yaw
            quat = (qw, qx, qy, qz)

            # Converting quaternions back to Euler angles roll, pitch and yaw
            rollMesured = math.atan2(2 * (qw * qx + qy * qz), 1 - 2 * (qx * qx + qy * qy))
            pitchMesured = math.asin(2 * (qw * qy - qz * qx))
            yawMesured = math.atan2(2 * (qw * qz + qx * qy), 1 - 2 * (qy * qy + qz * qz))

            rollNew = rollOld + rollMesured
            pitchNew = pitchOld + pitchMesured
            yawNew = yawOld + yawMesured
            buff = b''

            rollOld = rollNew
            pitchOld = pitchNew
            yawOld = yawNew

            rollToPrint = rollNew + toDeg
            pitchToPrint = pitchNew * toDeg
            yawToPrint = yawNew * toDeg

            print(rollToPrint, "  ", pitchToPrint, "  ", yawToPrint)

            continue
        if c == b'\r':
            c = bytes([s.read()[0] ^ 0x80])
        buff += c
