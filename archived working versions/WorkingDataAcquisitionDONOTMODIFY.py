'''
"archiving" this version 6/29/21 as a minimum-working-version
i.e. this implements the new NIDAQmx stuff but not very user-freindly for anyone but me 

when run as __main__ take_data(10 [iterations], 100,000 [Hz]) is called
modify last line of the file to change number of data sets collected or sampling frequency
data is saved at C:\\Users\\bjraiv23\\Desktop\\Experimental-Data\\[CURRENT DATE]\\[HH MM SS]
'''

import nidaqmx as nq
from nidaqmx import *
from nidaqmx.constants import AcquisitionType

import numpy as np
import os
import time

'''
# Wolfram stuff WILL work but less important right now

import WolframMathematicaAnalysisFunctions as wmaf

import logging
import warnings

#logging.basicConfig(level = logging.DEBUG)
#warnings.filterwarnings('ignore')
'''
def take_data(iterations, samp_rate):
 
  # measure ramp time
  time = meas_ramp_time()
  print('Ramp Time: ' + str(time) + ' seconds')

  # initialize task and configurations
  stream_reader = task_init(samp_rate, time)
  
  # create data array
  data = create_array(iterations, 2, samp_rate, time)
  
  # loop for iterations
  print('collecting ' + str(iterations) + ' sets of data')  
  for array in data:
      stream_reader.read_many_sample(array)
  
  # analyze data for peaks
  #peak_data = wmaf.fabry_perot_fit_frequency(data)
  try:
      #peak_data = wmaf.fabry_perot_fit_frequency(data)
      pass
  except:
      print('analysis failed')
      
  # write data to file
  save_data(data)
 

def task_init(samp_rate, time):  
    read_task = nq.Task()
    read_task.ai_channels.add_ai_voltage_chan('NI_PCIe-6351/ai0')
    read_task.ai_channels.add_ai_voltage_chan('NI_PCIe-6351/ai1')
    
    # expose task data stream and create Analog Multi Channel Reader
    in_stream = nq._task_modules.in_stream.InStream(read_task)
    reader = nq.stream_readers.AnalogMultiChannelReader(in_stream)
    
    read_task.timing.cfg_samp_clk_timing(samp_rate, sample_mode = AcquisitionType.FINITE, samps_per_chan = int(samp_rate * time))
    read_task.triggers.start_trigger.cfg_dig_edge_start_trig('/NI_PCIe-6351/PFI0')
    
    return reader

def meas_ramp_time():

    # create task to measure ramp time
    # add a pulse width counter channel, expose in_stream, and create reader
    time_task = nq.Task()
    time_task.ci_channels.add_ci_pulse_width_chan('NI_PCIe-6351/ctr0', 'pulse_width_channel', min_val= 0.01, max_val= 2)
    pulse_time_stream = nq._task_modules.in_stream.InStream(time_task)
    pulse_time_reader = nq.stream_readers.CounterReader(pulse_time_stream)
    
    # take sample, convert to seconds and return
    ticks = pulse_time_reader.read_one_sample_uint32()
    time_sec = ticks/100000000
    
    # close task
    time_task.close()
    
    return time_sec

def create_array(iterations, channels, samp_rate, time):
    '''
    returns data array (where the length of the array = iterations) of empty, identical, 
    pre-allocated numpy arrays (M*N where M = channels and N = samp_rate * time)
    '''
    data = []
    for i in range(iterations):
        data.append(np.empty((channels, int(samp_rate*time))))
    return data

def save_data(data):
    '''
    create a named and dated folder if one does not exist
    use os.mkdir which throws exception if folder already exists
    
    create a folder for each run with info and files (dialog) for each iteration

    '''
    date_time = time.ctime().split()
    day = date_time[0] + ' ' + date_time[1] + ' ' + date_time[2] + ', ' + date_time[4]
    current_time = date_time[3].split(':')[0] + ' ' + date_time[3].split(':')[1] + ' ' + date_time[3].split(':')[2]
    
    try:
        os.mkdir('C:\\Users\\bjraiv23\\Desktop\\Experimental-Data')
    except:
        pass 
    try:
        os.mkdir('C:\\Users\\bjraiv23\\Desktop\\Experimental-Data\\' + day)    
    except:
        pass
    try:
        os.mkdir('C:\\Users\\bjraiv23\\Desktop\\Experimental-Data\\' + day + '\\' + current_time)    
    except:
        pass
    
    for i in range(len(data)):
        #'C:\\Users\\bjraiv23\\Desktop\\Experimental-Data\\' + day + '\\' + current_time + '\\run' + str(i) + '.csv'
        file = open('C:\\Users\\bjraiv23\\Desktop\\Experimental-Data\\' + day + '\\' + current_time + '\\run' + str(i) + '.csv', 'w')
        for j in range(len(data[0][0])):
            file.write(str(data[i][0][j]) + ', ' + str(data[i][1][j]) +'\n')
            
        file.close()

if __name__ == "__main__":
    take_data(10, 100000)
