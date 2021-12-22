#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 16:13:52 2021

@author: selin
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


class SpectrumSimulator:
    
    def __init__(self, center, fwhm, fs, span):
        self.sigma = fwhm / 2*np.sqrt(2*np.log(2))
        self.center = center
        self.fs = 
        
        
        
        
        
        
        
            
            x_values = np.linspace(center-bw, center+bw, n)
            y_values = sc.stats.norm(center, standdevia)
            noize=np.random.randint(center, size=n)
            
    
    def splotting:
        filenum = 1000
        plt.plot(x_values, y_values.pdf(x_values)*noize)
            plt.xlabel(f'Frequency resolution over {n} points = {samprate/n} [Hz]', fontsize='small')
            plt.ylabel('Amplitude Density, [V/Hz^(1/2)]')
            savefile = 'SignalSimulation' + str(filenum) + '.png'
            plt.savefig(savefile)
            plt.clf()
            
            filenum+=1
        
        
        
        
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--center", type=float, nargs='?', help="Set local oscillator frequency")
    parser.add_argument("--fs", type=float, nargs='?', help="Set sampling rate")
    parser.add_argument("--span", type=float, nargs='?', help="Set span")
    parser.add_argument("--fwhm", type=int, nargs='?', help="Set full width half maximum")
    parser.add_argument("--filename", type=int, nargs='?', help="Set the filename for plot")
    args = parser.parse_args()
    SignalSim= SpectrumSimulator(args.center, args.bw, args.samprate, args.n)