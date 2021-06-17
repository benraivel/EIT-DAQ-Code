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
    
    # configure task sample timing
    timing = nq._task_modules.timing.Timing(read_task)
    timing.cfg_samp_clk_timing()
    
    # configure triggering (start and reference)
    trigger = nq._task_modules.triggering.start_trigger.StartTrigger(read_task)
    trigger.cfg_dig_edge_start_trig('NI_PCIe-6351/ctr0')
    
    # data array creation
    
    
    # return? other? 
    
    
    
def get_time():
    get_time_task = nq.Task()
    counter_channel = nq._task_modules.channels.ci_channel.CIChannel(get_time_task, 'ctr_chan')
    task_timing = nq._task_modules.timing.Timing(get_time_task)
    
    #configure implicit timing
    
    #set timebase source and rate
    counter_channel.ci_ctr_timebase_src
    counter_channel.
    
def run():
    pass

if __name__ == "__main__":
    print(get_time())