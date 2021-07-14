'''
- continuously acquire traces, averaging and displaying n traces
- create tkinter window:
    - mostly Mathematica graphic(s) of avg'd data
    - number-of-runs-to-average ajustable
    - sample rate adjustable
'''
import tkinter as tk
from tkinter import ttk

# import NI python API 
import nidaqmx as nq
from nidaqmx import *

import WolframSession as ws                                                                                                                                          

# import other modules
import numpy as np
import os
import time

class ContinuousAverage(ttk.Frame):

    def __init__(self, parent = None):
        
        self.meas_ramp_time()
             

    def run(self, n, sample_rate, time):
        buffer = np.empty(n)
        i = n
        while True:
            if i < n:
                i += 1
            else:
                i = 0
            np.insert(buffer, i, )

    def meas_ramp_time(self):
        ''' 
        measures pulse width of 691 nm ramp-sync square wave using ctr0
        
        signal must be connected to USER 1 and wired to PFI9
        
        returns time (s)
        '''
        # create Task to measure ramp time
        time_task = nq.Task()
        
        # add a pulse width counter channel using ctr0 
        # clock terminal default: 100 MHz internal | gate terminal default: PFI9
        # must connect signal to USER 1 BNC
        time_task.ci_channels.add_ci_pulse_width_chan('NI_PCIe-6351/ctr0', 'pulse_width_channel', min_val= 0.01, max_val= 2)
        
        # expose task in stream
        pulse_time_stream = nq._task_modules.in_stream.InStream(time_task)
        
        # create Counter Reader
        pulse_time_reader = nq.stream_readers.CounterReader(pulse_time_stream)
        
        # take sample and convert 100 MHz clock ticks to seconds
        ticks = pulse_time_reader.read_one_sample_uint32()
        time_sec = ticks/100000000
        
        # close task
        time_task.close()
        
        self.ramp_time = time_sec

    def task_init(self, samp_rate, time):
        ''' 
        creates and configures nidaqmx task for collecting data
        
        pass in sampling rate (Hz) and ramp time (s)
        
        returns AnalogMultiChannelReader
        '''
        # create analog data reading task
        read_task = nq.Task()
        
        # add channels (aio: difference signal | ai1: fabry perot)
        read_task.ai_channels.add_ai_voltage_chan('NI_PCIe-6351/ai0')
        read_task.ai_channels.add_ai_voltage_chan('NI_PCIe-6351/ai1')
        
        # expose task data stream
        in_stream = nq._task_modules.in_stream.InStream(read_task)
        
        # create Analog Multi Channel Reader
        reader = nq.stream_readers.AnalogMultiChannelReader(in_stream)
        
        # configure task timing (set sampling rate and number of samples to read)
        read_task.timing.cfg_samp_clk_timing(samp_rate, sample_mode = AcquisitionType.FINITE, samps_per_chan = int(samp_rate * time))
        
        # configure the start trigger (source: PFI0)
        read_task.triggers.start_trigger.cfg_dig_edge_start_trig('/NI_PCIe-6351/PFI0')
        
        return reader

    def create_array(self, iterations, channels, samp_rate, time):
        '''
        creates array of 2D arrays in memory to hold experimental data
        
        pass in number of times to run experiment (iterations), number of analog channels,
        sampling rate (Hz), and ramp time (s)
        
        returns data array (where length <= iterations) of empty, identical, 
        pre-allocated numpy arrays (M*N where M <= channels and N <= samp_rate * time)
        '''
        data = []
        for i in range(iterations):
            data.append(np.empty((channels, int(samp_rate*time))))
        return data