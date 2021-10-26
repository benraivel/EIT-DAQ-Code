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
from tkinter import messagebox as msg
from tkinter.constants import ANCHOR

# import NI python API 
import nidaqmx as nq
from nidaqmx import *

# import nidaqmx constants
from nidaqmx.constants import Signal, AcquisitionType

# import analysis functions
from EITAnalysis import fit_fabry_perot_peaks                                                                                                                                     

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
        self.__init_window()

    def __init_task(self, samp_rate, time, channel_str):
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

    def __init_window(self):
        '''
        create ttk widgets and arrange
        '''
         # create and grid tk/ttk frame with canvas to plot image
        self.scope_frame = ttk.Frame(self.parent)
        self.image_canvas = tk.Canvas(self.scope_frame, height = 643, width = 1000)
        self.image_canvas.grid(padx = 50, pady = 50)
        self.scope_frame.grid(row = 0)
        
        # create and grid control panel frame
        self.control_panel = ttk.LabelFrame(self.parent, text = 'Control Panel')
        self.control_panel.grid(row = 1)

        # create combobox to set analog channel
        channel_names = ['ai0', 'ai1', 'ai2', 'ai3', 'ai4', 'ai5', 'ai6', 'ai7']
        self.channel_select = ttk.Combobox(self.control_panel, values = channel_names)

        # create spinbox to set sampling frequency
        self.sample_freq_entry = ttk.Spinbox(self.control_panel, from_ = 1000, to = 1000000)

        # create spinbox to set runs-to-average
        self.runs_entry = ttk.Spinbox(self.control_panel, from_ = 1, to = 32)

        # create button widget to start acquiring
        self.start_button = ttk.Button(self.control_panel, text = 'Start', command = self.start)

        # label control panel widgets
        self.channel_label = ttk.Label(self.control_panel, text = 'Select analog\nin channel:')
        self.frequency_label = ttk.Label(self.control_panel, text = 'Set sampling\nfrequency (Hz):')
        self.runs_label = ttk.Label(self.control_panel, text = 'Set number of traces\nto average (1-32):')
        
        # arrange widgets in control panel with .grid():
        self.channel_label.grid(row = 0, column = 0)
        self.frequency_label.grid(row = 0, column = 1)
        self.runs_label.grid(row = 0, column = 2)
        self.start_button.grid(row = 0, column = 3, rowspan = 2)
        self.channel_select.grid(row = 1, column = 0)
        self.sample_freq_entry.grid(row = 1, column = 1)
        self.runs_entry.grid(row = 1, column = 2)
        
        # grid frame
        self.grid()

    def start(self):
        '''
        callback function of start button
        
        initializes all the user-specified parameters and raises error messages if needed

        creates data buffer 
        '''
        # try to measure ramp time
        try:
            self.meas_ramp_time()
        except:
            msg.showerror(title = 'NI-DAQmx Error', message = 'Ramp signal not detected')
            self.mainloop()

        # try to create task with user specified channel, sample rate, and measured time
        try:
            self.sample_frequency = int(self.sample_freq_entry.get())
            self.num_points = int(self.ramp_time * self.sample_frequency)
            self.__init_task(self.sample_frequency, self.ramp_time, self.channel_select.get())
        except:
            msg.showerror(title = 'NI-DAQmx Error', message = 'Could not create task with specified sample rate and channel')
            self.mainloop()

        # try to get runs-to-average and create buffer
        try:
            self.runs_to_avg = int(self.runs_entry.get())
            self.buffer = np.empty((self.runs_to_avg, 1, self.num_points))
            self.buffer_index = len(self.buffer)

            self.intercept_derivitive_buffer = np.empty(self.runs_to_avg)
        except:
            msg.showerror(title = 'Averaging Error', message = 'Could not create buffer with specified number of runs')
            self.mainloop()

        # make initial call to data reading function
        self.run()
       
    def run(self):
        '''
        data acquisition/analysis updating loop

        called continuously with delay >= ramp time

        manages the buffer, replacing the oldest trace with a newly acquired one
        '''
        # buffer index increment/loop
        if self.buffer_index < len(self.buffer) - 1:
            self.buffer_index += 1
        else:
            self.buffer_index = 0

        # pass correct array from buffer into stream reader
        self.reader.read_many_sample(self.buffer[self.buffer_index])
        
        # average the data in the buffer
        self.avg_data = self.average()

        # fit index to frequency(MHz) using average data
        try:
            if self.fit is not None:
                self.prev_fit = self.fit
        except:
            pass
        self.fit = fit_fabry_perot_peaks()

        # get plot image from data
        self.plot = self.session.listplot(self.avg_data)

        # draw image on canvas
        self.image_canvas.create_image((0,0), image = self.plot, anchor = tk.NW)
        
        # make recursive delayed call of read_data() so mainloop() can run freely
        self.image_canvas.after(int(self.ramp_time*1000), self.read_data)

    def average(self):
        '''
        averages data in buffer and returns as array
        '''
        temp = np.empty(self.num_points)
        for i in range(self.num_points):
            temp_val = 0.0
            for set in self.buffer:
                temp_val += set[0][i]
            temp[i] = temp_val/len(self.buffer)
        print(self.session.fit_fabry_perot_peaks(temp))
        return temp

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

    def close(self):
        root.destroy()

    def save_to_file(self, data, filename = None):
        # get and format date and time information
        date_time = time.ctime().split()
        day = date_time[1] + '_' + date_time[2] + '_' + date_time[4]
        current_time = date_time[3].split(':')[0] + ':' + date_time[3].split(':')[1] + ':' + date_time[3].split(':')[2]
        
        # try to create directories, pass if they already exist
        if self.directory == None:
            try:
                os.mkdir('C:\\Users\\bjraiv23\\Desktop\\Experimental-Data\\FabryPerotPeakData\\')
            except:
                pass 
            try:
                os.mkdir('C:\\Users\\bjraiv23\\Desktop\\Experimental-Data\\FabryPerotPeakData\\' + day)    
            except:
                pass
            try:
                self.directory = 'C:\\Users\\bjraiv23\\Desktop\\Experimental-Data\\FabryPerotPeakData\\' + day + '\\' + current_time
                os.mkdir(self.directory )  
            except:
                pass
        else:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    instance = ContinuousDisplay(root)
    root.protocol('WM_DELETE_WINDOW', instance.close)
    instance.mainloop()