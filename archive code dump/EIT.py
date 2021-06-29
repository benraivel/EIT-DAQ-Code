import nidaqmx as nq
from nidaqmx import *
#from nidaqmx.constants import 
import numpy as np
import os
import time


class Eit():
    
    def __init__ (self, experimental_iterations = 10, sample_clock_rate = 100000):
        
        self.task = nq.Task()
        self.channels = []
        self.sample_rate = sample_clk_rate
        self.iterations = experimental_iterations
        
        self.ramp_time = measure_pulse_time()
        
        
    
    
    def add_channel(self, name):
        self.channels.append(self.task.ai_channels.add_ai_voltage_chan('NI_PCIe-6351/' + name))
    
    
    
    
    def measure_pulse_time():
        ''' 
        creates task which uses a counter to measure ramp sync signal pulse-width 
        '''
        time_task = nq.Task()
        time_task.ci_channels.add_ci_pulse_width_chan('NI_PCIe-6351/ctr0', 'pulse_width_channel', min_val= 0.01, max_val= 2)
          
        pulse_time_stream = nq._task_modules.in_stream.InStream(time_task)
        pulse_time_reader = nq.stream_readers.CounterReader(pulse_time_stream)
          
        ticks = pulse_time_reader.read_one_sample_uint32()
        time_sec = ticks/100000000
          
        return time_sec
          
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
    
    def save_data(data):
        '''
        creates folders and writes files
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
