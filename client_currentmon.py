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
import datetime
from flask import Flask, render_template, request, redirect, url_for
import base64
from io import BytesIO
from matplotlib.figure import Figure



SECRET_KEY = 'ups'    
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def index():
    plot1, plot2, area1, area2 = plot_dcct()
    current1 = a1 * area1 
    current2 = a2 * area2
    return render_template('index2.html', plot2=plot2, plot1=plot1, current1=current1, current2=current2)#, form=form)

@app.route('/dcct', methods=('GET', 'POST'))
def dcct():
    global dcct
    global a1 
    global a2
    if isnum(request.form['dcct'])==True:
        if ',' in request.form['dcct']:
            dcct =  float(request.form['dcct'].replace(',', '.'))
            plot1, plot2, area1, area2 = plot_dcct()
            a1 = dcct/area1
            a2 = dcct/area2
            current1 = a1 * area1 
            current2 = a2 * area2
            return redirect(url_for('index', plot2=plot2, plot1=plot1, current1=current1, current2=current2))#, form=form))
        else:    
            dcct = float(request.form['dcct'])
            plot1, plot2, area1, area2 = plot_dcct()
            a1 = dcct/area1
            a2 = dcct/area2
            current1 = a1 * area1 
            current2 = a2 * area2
            return redirect(url_for('index', plot2=plot2, plot1=plot1, current1=current1, current2=current2))#, form=form))
    else:
        plot1, plot2, area1, area2 = plot_dcct()
        current1 = a1 * area1 
        current2 = a2 * area2
        return render_template('index2.html', error='Value must be numerical!', plot2=plot2, plot1=plot1, current1=current1, current2=current2)


def isnum(value):
        if value.isdigit():
            return True
        elif value.replace('.','').isdigit() or value.replace(',','').isdigit():
            return True
        else:
            return False

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
    ax.set_title(str(datetime.datetime.strptime(time.ctime(dates), "%a %b %d %H:%M:%S %Y"))+', DCCTnorm='+str(dcct))
    ax.set_xlabel('Frequency in [Hz]')
    ax.set_ylabel('Power in [dB]')
    ax.grid()
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
    ax2.set_title(str(datetime.datetime.strptime(time.ctime(dates2), "%a %b %d %H:%M:%S %Y"))+', DCCTnorm='+str(dcct))
    ax2.set_ylabel('Power in [dB]')
    ax2.set_xlabel('Frequency in [Hz]')
    ax2.grid()
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

def saveplot(ff, xx, dates):
    path = ''
    plt.plot(xx, ff, 'palevioletred')
   # plt.fill_betweenx(ff, xx[1], xx[-1], color='red')
    plt.xlabel('Frequency in [Hz]', fontsize='small')
    plt.ylabel('Power in [dB]')        
    plt.savefig(path + 'plot{}.png'.format(str(time.ctime(dates))+' DCCTmax='+str(dcct)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, nargs='?', help="Set publisher host")
    parser.add_argument("--port", type=str, nargs='?', help="Set publisher port")
    parser.add_argument("--hostCM", type=str, nargs='?', help="Set publisher host")
    parser.add_argument("--portCM", type=str, nargs='?', help="Set publisher port")
    args = parser.parse_args()
    port = args.port
    host = args.host
    a1, a2, dcct = 50, 50, 0.01
    app.run(debug=True, port=args.portCM, host=args.hostCM)
  
  
  
  
