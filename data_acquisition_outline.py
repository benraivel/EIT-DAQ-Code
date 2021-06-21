import nidaqmx as nq
from nidaqmx import *
#from nidaqmx.constants import 
import numpy as np
import os
import time

def take_data(iterations, samp_rate):
 
  # measure ramp time
  time = meas_ramp_time()
    
  # initialize task and configurations
  stream_reader = task_init(samp_rate, time)
  
  # create data array
  data = create_array(iterations, samp_rate, time)
  
  # loop for iterations
  
  for array in data:
      
      stream_reader.read_many_sample(array)
  
  # write data to file
  save_data(data)
  
  

def task_init(samp_rate, time):
    read_task = nq.Task()
    read_task.ai_channels.add_ai_voltage_chan('NI_PCIe-6351/ai0')
    read_task.ai_channels.add_ai_voltage_chan('NI_PCIe-6351/ai1')
    
    # expose task data stream and create Analog Multi Channel Reader
    in_stream = nq._task_modules.in_stream.InStream(read_task)
    reader = nq.stream_readers.AnalogMultiChannelReader(in_stream)
    
    # 
    timing = nq._task_modules.timing.Timing(read_task)
    
    timing.samp_clk_src = 
    timing.samp_clk_rate = 
    timing.cfg_samp_clk_timing(samp_rate)
    
     # configure triggering (start and reference)
    trigger = nq._task_modules.triggering.start_trigger.StartTrigger(read_task)
    trigger.cfg_dig_edge_start_trig('NI_PCIe-6351/PFI9')
    
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
    return time_sec
    
    # close task
    time_task.close()


def create_array(iterations, channels, samp_rate, time):
    '''
    returns data array (where the length of the array = iterations) of empty, identical, 
    pre-allocated numpy arrays (M*N where M = channels and N = samp_rate * time)
    '''
    data = []
    for i in range(iterations):
        data.append(np.empty((channels, int(samp_rate*time))))
    return data

def log():
    pass
    
def save_data(data):
    '''
    create a named and dated folder if one does not exist
    use os.mkdir which throws exception if folder already exists
    
    create a folder for each run with info and files (dialog) for each iteration

    '''
    date_time = time.ctime().split()
    day = date_time[0] + ' ' + date_time[1] + ' ' + date_time[2] + ', ' + date_time[4]
    current_time = date_time[3]
    
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
        data[i].tofile('C:\\Users\\bjraiv23\\Desktop\\Experimental-Data\\' + day + '\\' + current_time + '\\' + i + '.csv', sep = ',')

if __name__ == "__main__":
    take_data(10, 100000)