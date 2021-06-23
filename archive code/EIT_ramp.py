# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 12:36:54 2021

@author: bjraiv23

for synchronized writing and reading set the ai conversion clock to be the ao clock source
otherwise set the rate of ai clock with ai_conv_rate

start sampling off the first fabry perot peak??
    - use cfg_anlg_edge_start_trig and start sampling on the downward slope above trigger_level to get as close to the peak as possible

Genarally (I think):
    - Task
        
        start(), stop(), read(), write(), allows creation of event specific callback functions
        
        Task Modules:
            
        -Channel (less importan probably don't create directly)
        
            -Analog/digital in/out lots of parameters
            
        -Channel collection
        
            -create channels associated to physical inputs, determines 'type' of task
            give names to acess with Channel class?
            
        -Timing
            
        -Trigger
            
        -in_stream / out_stream  <=== control how in and out streams behave
        
            -stream reader/writer   <=== take experimental data here
"""
import numpy as np
import nidaqmx as nq
from nidaqmx import *
import math
import time
import threading

class EIT_Ramp():
    
    '''
        May want to make one class for writing and another for gathering data
            -1 task per object
            - add setters and getters, especially for clock sources/rates to make synchronization easy
            - in task.timing the ai_conv_src and ai_conv_timebase_src parameters
            
        need to fix issues with full ramp output, at lower sample frequencies entries are cut off
        similarly increasing frequency causes stretching
        may need to use sample clock timebase div for this 
        
    '''
    
    def __init__(self, vmin, vmax, ramp_freq, sample_freq, ramp_channel = 'ao0', data_channel = 'ai0'):
        
        self.min_voltage = vmin
        self.max_voltage = vmax
        self.ramp_frequency = ramp_freq
        self.sample_frequency = sample_freq
        
        # number of entries in ramp array is given by the desired frequency of the ramp and sampling clock frequency
        self.num_points = sample_freq//ramp_freq
        
        # Using Numpy linear space function create 1d array for ramp signal
        self.ramp = np.linspace(self.min_voltage, self.max_voltage, self.num_points)
        
        print(self.ramp)
        
        # Create a task? or maybe a global output channel
        
        # Two tasks, one for AO and one for AI
        self.write_task = nq.Task()
        self.read_task = nq.Task()
        
        # Add specified (or default) channels to respective tasks
        self.write_task.ao_channels.add_ao_voltage_chan('NI_PCIe-6351/'+ ramp_channel)
        self.read_task.ai_channels.add_ai_voltage_chan('NI_PCIe-6351/'+ data_channel)
        
        # expose out stream on write task and create Analog Single Channel Writer object
        self.out_stream = nq._task_modules.out_stream.OutStream(self.write_task)
        self.writer = nq.stream_writers.AnalogSingleChannelWriter(self.out_stream)
        
        # set sample clock frequency for tasks
        self.write_task.timing.cfg_samp_clk_timing(rate = self.sample_frequency, samps_per_chan = self.num_points)

    def get_write_task(self):
        return self.write_task
    
    def get_read_task(self):
        return self.read_task
    
    def write_ramp(self):
        
        self.write_task.start()
        self.write_task.write(self.ramp)
        self.write_task.stop()
        
    def add_ao_channel(self, channel_name):
         self.write_task.ao_channels.add_ao_voltage_chan('NI_PCIe-6351/'+ channel_name)
        

         
         
         
class Data_Reader():
    
    
    def __init__(self, channels = ['ai0']):
        
       self.read_task = nq.Task()
        
       for channel in channels:
           self.read_task.ai_channels.add_ai_voltage_chan('NI_PCIe-6351/'+ channel)
           
           
       self.in_stream = nq._task_modules.in_stream.InStream(self.read_task)
        

        
        
    def add_ai_channel(self, channel_name):
        
        self.read_task.ai_channels.add_ai_voltage_chan('NI_PCIe-6351/'+ channel_name)
    
        



        
### MAIN METHOD ###
# Test EIT_Ramp Class by creating an object and writing to output

if __name__ == "__main__":
    test1Hz = EIT_Ramp(-5,5,1,100000)
    while True:
        test1Hz.write_ramp()
    

