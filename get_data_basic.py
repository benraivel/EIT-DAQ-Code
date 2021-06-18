# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 09:26:19 2021

@author: bjraiv23

notes:
    - return data format: array of 2d data sets
    - use start and reference trigger
    - do not use the dynamic task.read
        -because am using stream_readers ==> need to pass pre allocated arrays
        
    - use apfi0 
    - want implicit timing
    - 

"""

import nidaqmx as nq
from nidaqmx import *
import numpy as np

def setup(): 
    '''
    creates the data reading Task() with 4 analog voltage channels,

    '''
    # create task for reading data and add data channels
    read_task = nq.Task()
    read_task.ai_channels.add_ai_voltage_chan('NI_PCIe-6351/ai0')
    read_task.ai_channels.add_ai_voltage_chan('NI_PCIe-6351/ai1')
    read_task.ai_channels.add_ai_voltage_chan('NI_PCIe-6351/ai2')
    read_task.ai_channels.add_ai_voltage_chan('NI_PCIe-6351/ai3')
    
    # expose task data stream and create Analog Multi Channel Reader
    in_stream = nq._task_modules.in_stream.InStream(read_task)
    reader = nq.stream_readers.AnalogMultiChannelReader(in_stream)
    
    # may want to use implicit timing because of the finite task?
    timing = nq._task_modules.timing.Timing(read_task)
    
    
    # configure triggering (start and reference)
    trigger = nq._task_modules.triggering.start_trigger.StartTrigger(read_task)
    trigger.cfg_dig_edge_start_trig()
    
    # data array creation
    
    
    # return? other? 
    
    
    
def get_time():
    
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
    
   
    
    
    
def run():
    pass

if __name__ == "__main__":
    print('Ramp Rise Time: ' + str(get_time()) + ' seconds')