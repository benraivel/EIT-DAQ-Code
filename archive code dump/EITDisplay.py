'''
New Class:
    - Creates tk window with 2 canvas/oscilliscope traces, one for the data and one for the fabry perot
    - using frequency fitting display traces in terms of frequency
    - data and fabry perot are averaged independently
    - robust derivative tracking
    - recording capability
    - user selects number of fp peaks visible
    - user sets resample resolution (Hz)
        - data array length: (peaks * 91.5 MHz) / resample resolution Hz
    - cast data: 
        - plug index into fit
        - divide result by resolution (integer division) to get new index
        - need to decide how to deal with doubled values
        - when all data has been added, create an interpolation?
        - could make it very big (kHz to Hz) then resample down then interpolate? to minimize interpolation (or interpolate alot try everything)
        - could display histogram to see number of points per resample bin or other way to quantify quality
        - put sucessive samples into large array
    
    display fabry perot in index units and data in freq units, show smoothed fp trace, points, and avg of a few
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
        calls setup functions
        '''
        # call parent init
        super().__init__(parent)
        self.parent = parent

        # create tk control variables
        self.__control_variables()

        # create and grid tk widgets
        self.__init_widgets()
        self.__gridding()

        # create wolfram evaluation session
        self.session = ws.WolframSession()

        # measure ramp time


    def close(self):
        '''
        window manager close callback

        ends wolfram session and destroys root
        '''
        self.session.end()
        root.destroy()


    def __ctrl_var(self):
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

        # resampling resolution (bin size in Hz)


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
        self.data_canvas = tk.Canvas(self.scope_frame, height = 643, width = 1000)
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



# main method
if __name__ == "__main__":
    root = tk.Tk()
    instance = EITDisplay(root)
    root.protocol('WM_DELETE_WINDOW', instance.close)
    instance.mainloop()