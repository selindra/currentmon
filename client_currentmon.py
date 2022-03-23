#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 15:55:44 2022

@author: selin
"""

import numpy as np
import argparse
import matplotlib.pyplot as plt
import zmq
import time
from flask import Flask, render_template, request
import base64
from io import BytesIO
from matplotlib.figure import Figure

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    plot1, plot2, area1, area2 = plot_dcct()
    return render_template('index2.html', plot2=plot2, plot1=plot1)

@app.route('/dcct', methods=['POST'])
def dcct():
    global dcct
    dcct = int(request.form['dcct'])
    plot1, plot2, area1, area2 = plot_dcct()
    
    return render_template('index2.html', plot2=plot2, plot1=plot1, area1=area1, area2=area2)
    

def plot_dcct():
    df,fd = getzmqdf()
    fs = int(np.real(df[0]))
    center = int(np.imag(df[0]))
    dates = int(np.real(df[1]))             
    df=df[2:]
    ff = abs(np.fft.fftshift(np.fft.fft(df)))**2
    xx = np.fft.fftshift(np.fft.fftfreq(fs, d=1/fs)) + center
    fig = Figure()
    ax = fig.subplots()
    ax.plot(xx , 10*np.log10(ff), 'palevioletred')
  #  ax.set_title(str(time.strftime("%H:%M:%S"))+' dcct='+str(dcct1))
    ax.set_title('Recorded on ' + str(time.ctime(dates))+' dcct='+str(dcct))
    ax.set_xlabel('Frequency in [Hz]')
    ax.set_ylabel('Power in [dB]')
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0) 
    figpng = base64.b64encode(buf.getvalue())
    area1 = np.trapz(ff,xx)/dcct    
    
    dates2 = int(np.real(fd[1])) 
    fd=fd[2:]
    ff2 = abs(np.fft.fftshift(np.fft.fft(fd)))**2
    fig2 = Figure()
    ax2 = fig2.subplots()
    ax2.plot(xx, 10*np.log10(ff2), 'palevioletred')
    ax2.set_title('Recorded on ' + str(time.ctime(dates2))+' dcct='+str(dcct))
    ax2.set_ylabel('Power in [dB]')
    ax2.set_xlabel('Frequency in [Hz]')
    buf2 = BytesIO()
    fig2.savefig(buf2, format="png")
    buf2.seek(0) 
    figpng2 = base64.b64encode(buf2.getvalue())
    area2 = np.trapz(ff2,xx)/dcct
    return figpng.decode("utf-8"), figpng2.decode("utf-8"), area1, area2

def getzmqdf():
    
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect('tcp://'+host+':'+port)
    socket.setsockopt(zmq.CONFLATE, 1)
    socket.setsockopt_string(zmq.SUBSCRIBE, '')
    dffd= socket.recv_pyobj()
    df = dffd[0:int(len(dffd)/2)]
    fd = dffd[int(len(dffd)/2):int(len(dffd)+1)]
    return df, fd

def saveplot(ff, xx):
    path = ''
    plt.plot(xx, ff, 'palevioletred')
     #  plt.fill_betweenx(ff, xx[1], xx[-1], color='red')
    plt.xlabel('Frequency [Hz]', fontsize='small')
    plt.ylabel('Power Density, [V^2/Hz]')        
    plt.savefig(path + 'plot{}.png'.format(str(time.strftime("%d.%m-%H:%M:%S"))))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dcct", type=float, nargs='?', help="Give the DCCT current value")
    parser.add_argument("--host", type=str, nargs='?', help="Set publisher host")
    parser.add_argument("--port", type=str, nargs='?', help="Set publisher port")
    parser.add_argument("--hostCM", type=str, nargs='?', help="Set publisher host")
    parser.add_argument("--portCM", type=str, nargs='?', help="Set publisher port")
    args = parser.parse_args()
    port = args.port
    host = args.host
    dcct = args.dcct
    app.run(debug=True, port=args.portCM, host=args.hostCM)
  
  
  
  
