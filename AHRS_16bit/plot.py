#!/usr/bin/env python3

import serial
import struct

import math

import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt

from collections import deque

from statistics import mean

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    plt.show()

    fig,axes = plt.subplots(2,2,sharex=True)
    axes[0][0].set_xlim(0, 100)
    axes[0][0].set_ylim(-5, +5)
    axes[1][0].set_ylim(-80000, +80000)
    axes[0][1].set_ylim(-5, +5)
    axes[1][1].set_ylim(-40000, +40000)

    x = 0
    y = 0
    datas = [ deque([y], maxlen=500) for _ in range(8)]
    datasflt = [ deque([(x, y)], maxlen=20000) for _ in range(8)]

    colours = ['b','g','r','c','m','y','b','b']
    axescnt = (axes[0][0],axes[0][0],axes[0][0],axes[1][0],axes[1][0],axes[1][0],axes[0][1],axes[1][1])
    labels = ('xg','yg','zg','xa','ya','za','normg','norma')

    lines = [ axe.plot(*zip(*data), c=colour, label=label)[0] for data,colour,axe,label in zip(datasflt,colours,axescnt,labels)]

    axes[0][0].legend()
    axes[1][0].legend()
    axes[0][1].legend()
    axes[1][1].legend()

    s = serial.Serial("/dev/ttyUSB2", 9600)
    buff = b''
    while s.read() != b'\n':
        pass

    while True:
        c = s.read()
        if c == b'\n':
            #print(buff, len(buff))
            raw = struct.unpack(">HHhhhhhhhHH", buff)
            print(raw)

            scalefactors=[0.025,0.025,0.025,2.45,2.45,2.45]
            scaled=[val*scale for val,scale in zip(raw[2:8],scalefactors)]
            

            datas[0].append(scaled[0])
            datas[1].append(scaled[1])
            datas[2].append(scaled[2])
            datas[3].append(scaled[3])
            datas[4].append(scaled[4])
            datas[5].append(scaled[5])
            datas[6].append(math.sqrt(sum([q**2 for q in scaled[0:3]])))
            datas[7].append(math.sqrt(sum([q**2 for q in scaled[3:6]])))

            datasflt[0].append((x, np.mean(datas[0])))
            datasflt[1].append((x, np.mean(datas[1])))
            datasflt[2].append((x, np.mean(datas[2])))
            datasflt[3].append((x, np.mean(datas[3])))
            datasflt[4].append((x, np.mean(datas[4])))
            datasflt[5].append((x, np.mean(datas[5])))
            datasflt[6].append((x, np.mean(datas[6])))
            datasflt[7].append((x, np.mean(datas[7])))


            x+=1

            if x%100 == 0:
                axes[0][0].relim()
                axes[0][0].autoscale_view()
                axes[1][0].relim()
                axes[1][0].autoscale_view()
                axes[0][1].relim()
                axes[0][1].autoscale_view()
                axes[1][1].relim()
                axes[1][1].autoscale_view()

                [line.set_data(*zip(*data)) for line,data in zip(lines,datasflt)]

                plt.draw()
                plt.pause(1e-30)

            buff=b''
            #s.reset_input_buffer()
            #while s.read() != b'\n':
            #    pass
            continue
        if c == b'\r':
            c = bytes([s.read()[0] ^ 0x80])
        buff += c


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
