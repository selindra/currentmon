#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 10:44:09 2021

@author: selin
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def makecomplexnp(filename):
    df = pd.read_csv(filename, header=None, sep='|')
    return np.array(df[0]+1j*df[1])[1:], float(df[0][0]),  int(df[1][0])


df,samplfreq, centrfreq = makecomplexnp(r'/Users/selin/Downloads/df1.csv')
n=1024
df=df[:n]

ff=np.fft.fft(df)
x = np.fft.fftfreq(n, d=1/samplfreq)

ff = abs(np.fft.fftshift(ff))**2
x = np.fft.fftshift(x) + centrfreq

plt.plot(x, ff)
area = np.trapz(ff,x)