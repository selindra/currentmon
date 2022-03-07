#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 11:22:40 2022

@author: selin
"""

from limereader import LimeReader
import numpy as np
import argparse
import matplotlib.pyplot as plt


def looper(center, span, dcct):
     
    mylime = LimeReader(center, 1, span*2, span*2, [1]) #span*2==fs???? and bw how related to span
    num=1
    try:
         while True:
             
            mylime.getsignal()
            df = mylime.convertsig()
            df = df[1:]
            n = int(span*2 * 1) 
            ff = abs(np.fft.fftshift(np.fft.fft(df)))**2
            xx = np.fft.fftshift(np.fft.fftfreq(n, d=1/span/2)) + center
            saveplot(ff, xx, num)
            num+=1
            area = np.trapz(ff,xx)/dcct
            print(area)
                 
    except(KeyboardInterrupt, EOFError):
        mylime.stopstream()
        print('Stream closed')
        
def saveplot(ff, xx, num):

    path = '/home/skye/Desktop/Marythes/LimeReader/plots/'
    plt.plot(xx, ff, 'c')
    plt.fill_betweenx(ff, xx[1], xx[-1], color='red')
    plt.xlabel('Frequency [Hz]', fontsize='small')
    plt.ylabel('Power Density, [V^2/Hz]')        
    plt.savefig(path + 'plot{:03}.png'.format(num))


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--center", type=float, nargs='?', help="Set local oscillator frequency")
  parser.add_argument("--span", type=float, nargs='?', help="Set span")
  parser.add_argument("--dcct", type=float, nargs='?', help="Give the DCCT current value")
  args = parser.parse_args()
  looper(args.center, args.span, args.dcct) 
   

   
    
    

        



