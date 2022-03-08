#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 11:32:35 2022

@author: selin
"""
from limereader import LimeReader
import zmq
import argparse
import time
import numpy as np
                
def con(host, port, center, span):
    
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind('tcp://'+host+':'+port)
    socket.setsockopt(zmq.CONFLATE, 1)
    mylime = LimeReader(args.center, 1, args.span*2, args.span, [1, 2]) #span*2==fs???? and bw how related to span
   
    try:
        while True:
                
            mylime.getsignal()
            df, fd = mylime.convertsig()
            dffd = np.append(df, fd)
            socket.send_pyobj(dffd)
            print('Sended at {}'.format(str(time.strftime("%d.%m-%H:%M:%S"))))

    except(KeyboardInterrupt, EOFError):
        mylime.stopstream()  
        print('Stream closed')  
      
if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--center", type=float, nargs='?', help="Set local oscillator frequency")
  parser.add_argument("--span", type=float, nargs='?', help="Set span")
  parser.add_argument("--host", type=str, nargs='?', help="Set publisher host")
  parser.add_argument("--port", type=str, nargs='?', help="Set publisher port")  
  args = parser.parse_args()
  con(args.host, args.port, args.center, args.span)

