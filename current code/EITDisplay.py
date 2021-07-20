'''
New Class:
    - Creates tk window with 2 canvas/oscilliscope traces, one for the data and one for the fabry perot
    - using frequency fitting display traces in terms of frequency
    - data and fabry perot are averaged independently
    - robust derivative tracking
    - recording capability
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

# import wolfram analysis functions
import WolframSession as ws                                                                                                                                          

# import other modules
import numpy as np
import os
import time

class EITDisplay(ttk.Frame):

    def __init__(self, parent = None):
        '''
        try to keep shorther than in ContinuousDisplay
        '''
        # call parent init
        super().__init__(parent)
        self.parent = parent

        # create tk control variables
        self.__control_variables()

        # create and grid tk widgets
        self.__init_widgets()
        self.__gridding()

        # measure ramp time


    def __control_variables(self):
        '''
        create tk control variables 
        '''
        # task sampling frequency
        self.samplefreq = tk.StringVar()
        self.samplefreq.set('100000')

        # ramp time (seconds)
        self.ramptime = tk.DoubleVar()

        # number of points
        self.numpoints = tk.IntVar()

        # number of fp peaks
        self.numpeaks = tk.IntVar()


    def __init_widgets(self):
        '''
        outsourced __init__ to contain widgets

        notes:
            - probably want to change aspect ratio, i.e. increase canvas pixel width
        '''
     ## Frames ##
        self.scope_frame = ttk.LabelFrame(self.parent)
        self.control_frame = ttk.LabelFrame(self.parent, text = 'Control Panel')
        self.analysis_frame = ttk.Frame(self.parent)

     ## Canvases ##
        self.fabryperot_canvas = tk.Canvas(self.scope_frame, height = 643, width = 1000)
        self.fabryperot_canvas = tk.Canvas(self.scope_frame, height = 643, width = 1000)

     ## Spinboxes ##
        self.numpeaks_spinbox = ttk.Spinbox(self.control_frame)
        self.samplefreq_spinbox = ttk.Spinbox(self.control_frame, textvariable = self.samplefreq)

     ## Buttons ##
        self.retime_button = ttk.Button(self.control_frame, text = 'Retime Ramp', command = self.meas_ramp_time)


    def __gridding(self):
        '''
        outsourced __init__ gridding 
        '''
        pass


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
        
        self.ramptime = time_sec

# Main method
if __name__ == "__main__":
    root = tk.Tk()
    instance = EITDisplay(root)
    root.protocol('WM_DELETE_WINDOW', instance.close)
    instance.mainloop()