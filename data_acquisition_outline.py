import nidaqmx as nq
from nidaqmx import *
import numpy as np

def take_data(iterations, samp_rate, filename):
  
  # initialize task and configurations
  task_init()
  
  # measure ramp time
  time = meas_ramp_time()
  
  # create data array
  data = create_array(iterations, samp_rate, time)
  
  # loop for iterations
  
# function code mostly here
  
  # write data to file
  write_file(filename, data)
  
  pass

def task_init():
  pass

def meas_ramp_time():
    
   # create task to measure ramp time
    time_task = nq.Task()
    
    # add a pulse width counter channel to the task
    time_task.ci_channels.add_ci_pulse_width_chan('NI_PCIe-6351/ctr0', 'pulse_width_channel', min_val= 0.01, max_val= 2)
    
    pulse_time_stream = nq._task_modules.in_stream.InStream(time_task)
    
    pulse_time_reader = nq.stream_readers.CounterReader(pulse_time_stream)
    
    ticks = pulse_time_reader.read_one_sample_uint32()
    
    time_sec = ticks/100000000
    
    return time_sec

    time_task.close()

def create_array(iterations, samp_rate, time):
  

def write_file(filename, data):
  pass

if __name__ == "__main__":
    pass