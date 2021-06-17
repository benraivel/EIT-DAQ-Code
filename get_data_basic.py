# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 09:26:19 2021

@author: bjraiv23

notes:
    
    - return data format: array of 2d data sets


"""

import nidaqmx as nq
from nidaqmx import *
import numpy as np

def setup(): 
    read_task = nq.Task()
    read_task.ai_channels.add_ai_voltage_chan('NI_PCIe-6351/ai0')
    
    trigger = nq._task_modules.triggering.start_trigger.StartTrigger(read_task)
    print(trigger)
    trigger.cfg_dig_edge_start_trig('NI_PCIe-6351/di0')
    
    timing = nq._task_modules.timing.Timing(read_task)
  # timing.cfg_samp_clk_timing()
    
    in_stream = nq._task_modules.in_stream.InStream(read_task)
    
    reader = nq.stream_readers.AnalogMultiChannelReader(in_stream)
    
def get_freq():
    
    # add ctr task
    ramp_freq_task = nq.Task()
    
    # create ci channel
    ci_channel = ramp_freq_task.ci_channels.add_ci_freq_chan('NI_PCIe-6351/ctr0', min_val = 0.5, max_val = 20, meas_time = 20)
    
    # set up signal filtering
    ci_channel.ci_freq_dig_fltr_enable = True
    
    # set up timing
    freq_timing = nq._task_modules.timing.Timing(ramp_freq_task)
    
    #expose stream
    freq_stream = nq._task_modules.in_stream.InStream(ramp_freq_task)
    
    # create reader
    freq_reader = nq.stream_readers.CounterReader(freq_stream)
    
    return 
    
def run():
    pass

if __name__ == "__main__":
    setup()