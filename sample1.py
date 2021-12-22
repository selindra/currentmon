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
n=2048
df=df[:n]

# ff=np.fft.fft(df)
# x = np.fft.fftfreq(n, d=1/samplfreq)
# plt.plot(x, ff, 'palevioletred')
# plt.xlabel(f'Frequency resolution over {n} points = {samplfreq/n} [Hz]', fontsize='small')
# plt.ylabel('Amplitude Density, [V/Hz^(1/2)]')



ff = abs(np.fft.fftshift(np.fft.fft(df)))**2
x = np.fft.fftshift(np.fft.fftfreq(n, d=1/samplfreq)) + centrfreq
plt.plot(x, ff, 'palevioletred')
plt.xlabel(f'Frequency resolution over {n} points = {samplfreq/n} [Hz]', fontsize='small')
plt.ylabel('Power Density, [V^2/Hz]')

area = np.trapz(ff,x)