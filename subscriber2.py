#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 12:28:01 2022

@author: selin
"""

import numpy as np
import argparse
import matplotlib.pyplot as plt
import zmq
import time


def areacalc(dcct, host, port): 
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    #socket.connect ("tcp://localhost:5556s")
    socket.connect('tcp://'+host+':'+port)
    socket.setsockopt(zmq.CONFLATE, 1)
    socket.setsockopt_string(zmq.SUBSCRIBE, '')

    print('connected to publisher')
    while True:
        df = socket.recv_pyobj()
   #    print(df)
        fs = int(np.real(df[0]))
        center = int(np.imag(df[0]))
        df=df[1:]
        ff = abs(np.fft.fftshift(np.fft.fft(df)))**2
        xx = np.fft.fftshift(np.fft.fftfreq(fs, d=1/fs)) + center
        saveplot(ff, xx)
        area = np.trapz(ff,xx)/dcct
        print(area)
                    
def saveplot(ff, xx):
    path = '/home/skye/Desktop/Marythes/LimeReader/plots/'
    plt.plot(xx, ff, 'palevioletred')
 #  plt.fill_betweenx(ff, xx[1], xx[-1], color='red')
    plt.xlabel('Frequency [Hz]', fontsize='small')
    plt.ylabel('Power Density, [V^2/Hz]')        
    plt.savefig(path + 'plot{}.png'.format(str(time.strftime("%d.%m-%H:%M:%S"))))


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
# parser.add_argument("--center", type=float, nargs='?', help="Set local oscillator frequency")
# parser.add_argument("--span", type=float, nargs='?', help="Set span")
  parser.add_argument("--dcct", type=float, nargs='?', help="Give the DCCT current value")
  parser.add_argument("--host", type=str, nargs='?', help="Set publisher host")
  parser.add_argument("--port", type=str, nargs='?', help="Set publisher port")
  args = parser.parse_args()
  areacalc(args.dcct, args.host, args.port) 
  
  
  
  
  
