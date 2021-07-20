'''
- similar to wolframsession try to contain nq api usage
'''

# import NI python API 
import nidaqmx as nq
from nidaqmx import _task_modules, stream_readers, stream_writers
from nidaqmx._task_modules import timing, in_stream, out_stream, triggers

# import nidaqmx constants
from nidaqmx.constants import Signal, AcquisitionType

# import message stuff
from tkinter import messagebox as msg

class NQTask():

    def __init__(self, device = 'NI_PCIe-6351', ai_channels = None, ao_channels = None, ci_channels = None, co_channels = None, di_channels = None, do_channels = None):
        '''
        a universal initializer for nidaqmx tasks, creates task with name

        for only one of the channel parameters (ai_channels, ao_channels, ci_channels, co_channels, di_channels, do_channels): 
            - pass in a string i.e. 'ai0' or list of strings
            - creates
        '''
        # create generic task
        self.task = nq.Task()

        # make analog in task
        if ai_channels is not None:
            
            # init single channel
            if isinstance(ai_channels, str):
                
                # add channel
                self.task.ai_channels.add_ai_voltage_chan(device + '/' + ai_channels)

                # create stream
                self.stream = in_stream.InStream(self.task)

                # create reader
                self.reader = stream_readers.AnalogSingleChannelReader(self.stream)

            # init multi channel
            elif isinstance(ai_channels, list):

                # add channels
                for channel in ai_channels:
                    self.task.ai_channels.add_ai_voltage_chan(device + '/' + channel)
                
                # create stream
                self.stream = in_stream.InStream(self.task)

                # create reader
                self.reader = stream_readers.AnalogMultiChannelReader(self.stream)

        # make analog out task
        elif ao_channels is not None:
            
            # init single channel
            if isinstance(ao_channels, str):
                self.task.ao_channels.add_ao_voltage_chan(device + '/' + ao_channels)

            # init multi channel
            elif isinstance(ao_channels, list):
                for channel in ao_channels:
                    self.task.ao_channels.add_ao_voltage_chan(device + '/' + channel)

        # make counter in task
        elif ci_channels is not None:
            pass

        # make counter out task
        elif co_channels is not None:
            pass

        # make digital in task
        elif di_channels is not None:
            pass

        # make digital out task
        elif do_channels is not None:
            pass
        
        # error message
        else:
            msg.showerror(title = 'Task Create Error!', message = 'Pass in a string symbolizing a channel or list of strings for only one of parameters:\nai_channels, ao_channels, ci_channels, co_channels, di_channels, do_channels')


    def cfg_timing(self, rate, finite = True, samples = None):
        '''
        configure the timing for the task
        '''
        if finite:
            self.task.timing.cfg_samp_clk_timing(rate, sample_mode = AcquisitionType.FINITE)

if __name__ == "__main__":
    NQTask()

