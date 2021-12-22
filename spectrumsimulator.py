#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 16:13:52 2021

@author: selin
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy as sc
from scipy import stats
import argparse
from time import sleep, time

class SpectrumSimulator:
    
    def __init__(self, center, time, bw, samprate, n):
        
        filenum = 1000
        
        while True:
            standdevia=bw/10
            x_values = np.linspace(center-bw, center+bw, n)
            y_values = sc.stats.norm(center, standdevia)
            noize=np.random.randint(center, size=n)
            plt.plot(x_values, y_values.pdf(x_values)*noize)
            plt.xlabel(f'Frequency resolution over {n} points = {samprate/n} [Hz]', fontsize='small')
            plt.ylabel('Amplitude Density, [V/Hz^(1/2)]')
            savefile = 'SignalSimulation' + str(filenum) + '.png'
            plt.savefig(savefile)
            plt.clf()
            filenum+=1
            sleep(float(time))
        
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--center", type=float, nargs='?', help="Set local oscillator frequency")
    parser.add_argument("--time", type=int, nargs='?', help="Set measurement time")
    parser.add_argument("--samprate", type=float, nargs='?', help="Set sampling rate")
    parser.add_argument("--bw", type=float, nargs='?', help="Set bandwidth")
    parser.add_argument("--n", type=int, nargs='?', help="Set number of points")
    args = parser.parse_args()
    SignalSim= SpectrumSimulator(args.center, args.time, args.bw, args.samprate, args.n)