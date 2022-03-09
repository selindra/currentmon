#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 16:13:52 2021

@author: selin
"""
import numpy as np
import matplotlib.pyplot as plt
import argparse
from scipy import stats

class SpectrumSimulator:
    
    def __init__(self, center, fwhm, span, n):
        
        self.center = center
        self.fwhm = fwhm
        self.sigma = fwhm / 2*np.sqrt(2*np.log(2))
        self.span = span
        self.n = n
    
    def get_spectrum(self):     
        x_values = np.linspace(self.center-self.span, self.center+self.span, int(self.n))
        y_values = stats.norm(self.center, self.sigma)
        noise = np.random.randint(self.center, size = self.n)
        return x_values, y_values.pdf(x_values)*noise

    def splotting(self, x_values, y_values, filename):
        plt.plot(x_values, y_values)
        plt.xlabel('Frequency, Hz')
        plt.ylabel('Power Density, [a. u.]')
        plt.savefig(f'{filename}.png')
        
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--center", type=float, nargs='?', help="Set local oscillator frequency")
    parser.add_argument("--span", type=float, nargs='?', help="Set span")
    parser.add_argument("--fwhm", type=float, nargs='?', help="Set full width half maximum")
    parser.add_argument("--filename", type=str, nargs='?', help="Set the filename for plot")
    parser.add_argument("--n", type=int, nargs='?', help="Set the number of points")
    args = parser.parse_args()
    
    spectrum_sim = SpectrumSimulator(args.center, args.fwhm, args.span, args.n)
    xx, yy = spectrum_sim.get_spectrum()
    spectrum_sim.splotting(xx, yy, args.filename)
    
    