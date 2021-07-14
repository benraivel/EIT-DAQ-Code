'''
- continuously acquire traces, averaging and displaying n traces
- create tkinter window:
    - mostly Mathematica graphic(s) of avg'd data
    - number-of-runs-to-average ajustable
    - sample rate adjustable
- use mathematica image() to create bitmap to transfer via client instead of saving
    - ImageData[Image[ListPlot[data[[1]], PlotRange -> Full, ImageSize -> Large], ImageResolution -> 500]]
- numpy asarray to convert to array
- PIL.Image.fromarray()
'''
# import graphics
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# import NI python API 
import nidaqmx as nq
from nidaqmx import *

# import nidaqmx constants
from nidaqmx.constants import Signal, AcquisitionType

# import wolfram analysis functions
import WolframSession as ws                                                                                                                                          

# import other modules
import numpy as np
import os
import time


class ContinuousDisplay(ttk.Frame):

    def __init__(self, parent = None):
        '''
        creates graphics window, entry boxes for parameters, and start button
        '''
        # call parent init
        super().__init__(parent)
        self.parent = parent

        # create and grid tk/ttk frame with canvas to plot image
        self.scope_frame = ttk.Frame(self.parent, height = 2520, width = 4000)
        self.image_canvas = tk.Canvas(self.scope_frame, height = 2520, width = 4000)
        self.scope_frame.grid(row = 0)
        
        # create and grid frame for controls
        self.control_panel = ttk.Frame(self.parent)
        self.control_panel.grid(row = 1)

        # create spinbox to set sampling frequency
        self.sample_freq_entry = ttk.Spinbox(self.control_panel, from_ = 1000, to = 500000)

        # create spinbox to set runs-to-average
        self.runs_entry = ttk.Spinbox(self.control_panel, from_ = 1, to = 16)

        # create combobox to set analog channel
        channel_names = ['ai0', 'ai1', 'ai2', 'ai3', 'ai4', 'ai5', 'ai6', 'ai7']
        self.channel_select = ttk.Combobox(self.control_panel, values = channel_names)
        
        # create button widget to start acquiring
        self.start_button = ttk.Button(self.control_panel, command = self.run)

        # arrange widgets in window with .grid():
        #   row 0:
        self.image_canvas.grid(row = 0, column = 0, columnspan = 4)
        #   row 1:
        self.channel_select.grid(row = 1, column = 0)
        self.sample_freq_entry.grid(row = 1, column = 1)
        self.runs_entry.grid(row = 1, column = 2)
        self.start_button.grid(row = 1, column = 3)
        
        # create wolfram evaluation session to create plots
        self.session = ws.WolframSession()

  

    def run(self):
        '''
        try to set up task using entry widget values
        '''
        
        try:
            self.meas_ramp_time()
        except:
            pass
        
        self.meas_ramp_time()

        self.num_points = self.ramp_time * self.sample_freq_entry.get()
        self.num_runs = self.runs_entry.get()

        self.buffer = np.empty(n)

        i = n

        while True:
            if i < n:
                i += 1
            else:
                i = 0
            np.insert(self.buffer, i, )

            self.reader.read_many_sample()


    def average(self):
        '''
        - averages data in buffer
        '''
        temp = []
        for i in range(self.num_points):
            temp_val = 0.0
            for set in self.buffer:
                temp_val += set[i]
            temp[i] = temp_val/self.num_runs



    def meas_ramp_time(self):
        ''' 
        - measures pulse width of 691 nm ramp-sync square wave using ctr0
        
        - signal must be connected to USER 1 and wired to PFI9
        
        - returns time (s)
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


    def task_init(self, samp_rate, time, channel_str):
        ''' 
        creates and configures nidaqmx task for collecting data
        
        pass in sampling rate (Hz) and ramp time (s)
        
        creates self.reader
        '''
        # create analog data reading task
        self.task = nq.Task()
        
        # add channels (aio: difference signal | ai1: fabry perot)
        self.task.ai_channels.add_ai_voltage_chan('NI_PCIe-6351/' + channel_str)
        
        # expose task data stream
        in_stream = nq._task_modules.in_stream.InStream(self.task)
        
        # create Analog Multi Channel Reader
        self.reader = nq.stream_readers.AnalogMultiChannelReader(in_stream)
        
        # configure task timing (set sampling rate and number of samples to read)
        self.task.timing.cfg_samp_clk_timing(samp_rate, sample_mode = AcquisitionType.FINITE, samps_per_chan = int(samp_rate * time))
        
        # configure the start trigger (source: PFI0)
        self.task.triggers.start_trigger.cfg_dig_edge_start_trig('/NI_PCIe-6351/PFI0')

        # add callback for start trigger to perform analysis / scope updates
        

    def create_array(self, iterations, channels, samp_rate, time):
        '''
        creates array of 2D arrays in memory to hold experimental data
        
        pass in number of times to run experiment (iterations), number of analog channels,
        sampling rate (Hz), and ramp time (s)
        
        creates self.data array (where length <= iterations) of empty, identical, 
        pre-allocated numpy arrays (M*N where M <= channels and N <= samp_rate * time)
        '''
        self.data = []

        for i in range(iterations):
            self.data.append(np.empty((channels, int(samp_rate*time))))
        




if __name__ == "__main__":
    root = tk.Tk()
    instance = ContinuousDisplay(root)
    instance.mainloop()