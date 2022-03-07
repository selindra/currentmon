import numpy as np
import argparse
import SoapySDR
from SoapySDR import SOAPY_SDR_RX, SOAPY_SDR_CS16
import time 

class LimeReader:
  #at first one has to initialize SDR. Init method sets all preferences and setups the data streams
  def __init__(self, cent_freq, meas_time, fs, rx_bw, channel): #rx_bw - bandwidth, fs - sampling rate
    self.channel = channel
    self.freq = cent_freq            # LO tuning frequency in Hz
    self.timeout_us = int(5e6)
    self.n = int(fs * meas_time)               # Number of complex samples per transfer
    self.rx_bits = 12            # The Lime's ADC is 12 bits
    RX1 = 0             # RX1 = 0, RX2 = 1
    RX2 = 1
    self.fs=fs
    self.sdr = SoapySDR.Device(dict(driver="lime")) # Create AIR-T instance
      
    if (len(self.channel) == 2):
      self.sdr.setSampleRate(SOAPY_SDR_RX, RX1, fs)   # Set sample rate
      self.sdr.setSampleRate(SOAPY_SDR_RX, RX2, fs)          
      self.sdr.setGainMode(SOAPY_SDR_RX, RX1, True)   # Set the gain mode
      self.sdr.setGainMode(SOAPY_SDR_RX, RX2, True)
      self.sdr.setGain(SOAPY_SDR_RX, RX1, "TIA", 0) # Set TransImpedance Amplifier gain
      self.sdr.setGain(SOAPY_SDR_RX, RX2, "TIA", 0)    
      self.sdr.setGain(SOAPY_SDR_RX, RX1, "LNA", 0) # Set Low-Noise Amplifier gain
      self.sdr.setGain(SOAPY_SDR_RX, RX2, "LNA", 0)      
      self.sdr.setGain(SOAPY_SDR_RX, RX1, "PGA", 0) # programmable-gain amplifier (PGA)
      self.sdr.setGain(SOAPY_SDR_RX, RX2, "PGA", 0)       
      
      # self.sdr.setGain(SOAPY_SDR_RX, RX1, 0)
      # self.sdr.setGain(SOAPY_SDR_RX, RX2, 0) 
      # self.sdr.setDCOffsetMode(SOAPY_SDR_RX, 0, False)  
      # self.sdr.setDCOffsetMode(SOAPY_SDR_RX, 1, False)
      
      self.sdr.setFrequency(SOAPY_SDR_RX, RX1, self.freq)         # Tune the LO
      self.sdr.setFrequency(SOAPY_SDR_RX, RX2, self.freq)         # Tune the LO
      self.RX1_buff = np.empty(2 * self.n, np.int16)                 # Create memory buffer for data stream
      self.RX2_buff = np.empty(2 * self.n, np.int16)                 # Create memory buffer for data stream
      self.sdr.setBandwidth(SOAPY_SDR_RX, RX1, rx_bw)
      self.sdr.setBandwidth(SOAPY_SDR_RX, RX2, rx_bw)
      self.sdr.setAntenna(SOAPY_SDR_RX, RX1, "LNAL")
      self.sdr.setAntenna(SOAPY_SDR_RX, RX2, "LNAL")
      # Create data buffer and start streaming samples to it
      self.rx_stream = self.sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CS16, [RX1, RX2])
      time.sleep(0.8)
      # Setup data stream
    
    elif(self.channel[0] == 1):
      self.sdr.setSampleRate(SOAPY_SDR_RX, RX1, fs)          # Set sample rate
      self.sdr.setGainMode(SOAPY_SDR_RX, RX1, True)       # Set the gain mode
      self.sdr.setGain(SOAPY_SDR_RX, RX1, "TIA", 0)
      self.sdr.setGain(SOAPY_SDR_RX, RX1, "LNA", 0)
      self.sdr.setGain(SOAPY_SDR_RX, RX1, "PGA", 0) # programmable-gain amplifier (PGA)
      self.sdr.setFrequency(SOAPY_SDR_RX, RX1, self.freq)         # Tune the LO    
      self.RX1_buff = np.empty(2 * self.n, np.int16)                 # Create memory buffer for data stream
      self.sdr.setBandwidth(SOAPY_SDR_RX, RX1, rx_bw)
      self.sdr.setAntenna(SOAPY_SDR_RX, RX1, "LNAL")
      self.rx_stream = self.sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CS16, [RX1])
      time.sleep(0.8)
      # Setup data stream
     
   
    elif(self.channel[0] == 2):
      self.sdr.setSampleRate(SOAPY_SDR_RX, RX2, fs)          # Set sample rate
      self.sdr.setGainMode(SOAPY_SDR_RX, RX2, True)       # Set the gain mode
      self.sdr.setGain(SOAPY_SDR_RX, RX2, "TIA", 0)
      self.sdr.setGain(SOAPY_SDR_RX, RX2, "LNA", 0)
      self.sdr.setGain(SOAPY_SDR_RX, RX2, "PGA", 0) # programmable-gain amplifier (PGA)
      self.sdr.setFrequency(SOAPY_SDR_RX, RX2, self.freq)         # Tune the LO    
      self.RX2_buff = np.empty(2 * self.n, np.int16)                 # Create memory buffer for data stream
      self.sdr.setBandwidth(SOAPY_SDR_RX, RX2, rx_bw)
      self.sdr.setAntnenna(SOAPY_SDR_RX, RX2, "LNAL")
      self.rx_stream = self.sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CS16, [RX2])
      time.sleep(0.8)
      # Setup data stream
   
    else:
      raise ValueError("Channel amount has to be 1 or 2")
      

  #this function reads stream of data and puts it in self.rx_stream numpy array   
  def getsignal(self):
    #  Initialize the AIR-T receiver using SoapyAIRT
    self.sdr.activateStream(self.rx_stream)  # this turns the radio on
     # Read the samples from the data buffer
    if (len(self.channel) == 2):
      sr = self.sdr.readStream(self.rx_stream, [self.RX1_buff, self.RX2_buff], self.n, timeoutUs = self.timeout_us)
    elif(self.channel[0] == 1):
      sr = self.sdr.readStream(self.rx_stream, [self.RX1_buff], self.n, timeoutUs = self.timeout_us)    
    elif(self.channel[0] == 2):
      sr = self.sdr.readStream(self.rx_stream, [self.RX2_buff], self.n, timeoutUs = self.timeout_us)
  
    rc = sr.ret # number of samples read or the error code
    assert rc == self.n, 'Error Reading Samples from Device (error code = %d)!' % rc
   
    # Stop stream
  def stopstream(self):
    self.sdr.deactivateStream(self.rx_stream)
    self.sdr.closeStream(self.rx_stream)
    
  #this function makes complex64 from ADC bits and saves it as binary file  
  def convertsig(self):
    if (len(self.channel) == 2):
    # Convert interleaved shorts (received signal) to numpy.complex64 normalized between [-1, 1]
      RX1bits = self.RX1_buff.astype(float) / np.power(2.0, self.rx_bits-1)
      RX2bits = self.RX2_buff.astype(float) / np.power(2.0, self.rx_bits-1)
      # RX1complex = (RX1bits[::2] + 1j*RX1bits[1::2]).astype(np.complex64) 
      # RX2complex = (RX2bits[::2] + 1j*RX2bits[1::2]).astype(np.complex64)
      RX1complex = (RX1bits[::2] + 1j*RX1bits[1::2])
      RX2complex = (RX2bits[::2] + 1j*RX2bits[1::2])
      RX1complex = np.insert(RX1complex, 0, (self.fs + 1j*self.freq) )
      RX2complex = np.insert(RX2complex, 0, (self.fs + 1j*self.freq) )
      self.RX1complex = np.complex64(RX1complex)
      self.RX2complex = np.complex64(RX2complex)
      return RX1complex, RX2complex
   
    elif(self.channel[0] == 1):
      RX1bits = self.RX1_buff.astype(float) / np.power(2.0, self.rx_bits-1)
      RX1complex = (RX1bits[::2] + 1j*RX1bits[1::2]) 
      RX1complex = np.insert(RX1complex, 0, (self.fs + 1j*self.freq) )
      self.RX1complex = np.complex64(RX1complex)
      return RX1complex
   
    elif(self.channel[0] == 2):
      RX2bits = self.RX2_buff.astype(float) / np.power(2.0, self.rx_bits-1)
      RX2complex = (RX2bits[::2] + 1j*RX2bits[1::2]) 
      RX2complex = np.insert(RX2complex, 0, (self.fs+ 1j*self.freq) )
      self.RX2complex = np.complex64(RX2complex)
      return RX2complex

  def savetofile(self, filenames):
    if(len(self.channel) == 2):
      self.RX1complex.tofile(filenames[0])
      self.RX2complex.tofile(filenames[1])
    elif(self.channel[0] == 1):
      self.RX1complex.tofile(filenames[0])
    elif(self.channel[0] == 2):
      self.RX2complex.tofile(filenames[0])


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--center", type=float, nargs='?', help="Set local oscillator frequency")
  parser.add_argument("--time", type=int, nargs='?', help="Set measurement time")
  parser.add_argument("--fs", type=float, nargs='?', help="Set sampling rate")
  parser.add_argument("--bw", type=float, nargs='?', help="Set bandwidth")
  parser.add_argument("--channel", type=int, nargs='+', help="Set channels to read data from")
  parser.add_argument("--filename", type=str, action='append', nargs='+', help="Path to saved file")
  args = parser.parse_args()
  
  if args.time and args.fs and args.filename and args.channel and args.bw:
    print ("Central frequency set to ", args.center, " Hz.")
    print ("Measurement time set to ", args.time, " sec.")
    print ("Sampling rate set to ", args.fs, " Samples/sec.")
    print ("Bandwidth set to ", args.bw, " Hz.")

    if ( len(args.channel) == len(args.filename[0]) and len(args.channel) == 1 ):
      print ("Reading from channels ", args.channel[0])
      print ("file saved as: ", args.filename[0][0])
      #initialize Lime SDR with entered measure time, bandwidth, sampling rate
      Lime = LimeReader(args.center, args.time, args.fs, args.bw, args.channel) 
      Lime.getsignal()
      Lime.stopstream()
      Lime.convertsig()
      Lime.savetofile(args.filename[0])
    
    elif ( len(args.channel) == len(args.filename[0]) and len(args.channel) == 2 ):
      print ("Reading from channels ", args.channel[0],args.channel[1])
      print ("file saved as: ", args.filename[0][0], args.filename[0][1])
  #initialize Lime SDR with entered measure time, bandwidth, sampling rate
      Lime = LimeReader(args.center, args.time, args.fs, args.bw, args.channel) 
      Lime.getsignal()
      Lime.stopstream()
      Lime.convertsig()
      Lime.savetofile(args.filename[0])
      
      
    
    else:
      print ("channels amount not equal to amount of files")     
  else:
    print ("No parameters were given")

