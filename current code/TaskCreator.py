'''
general purpose task constructor
'''
# import NI python API 
import nidaqmx as nq
from nidaqmx import _task_modules, stream_readers, stream_writers
from nidaqmx._task_modules import timing, in_stream, out_stream, triggers
from nidaqmx._task_modules.channels.ai_channel import AIChannel

# import nidaqmx constants
from nidaqmx.constants import Signal, AcquisitionType

# import message stuff
from tkinter import messagebox as msg

class NQTask():

 ## main init function ##

    def __init__(self, device = 'NI_PCIe-6351', ai_channels = None, ao_channels = None, ci_channels = None, co_channels = None, di_channels = None, do_channels = None):
        '''
        a universal initializer for nidaqmx tasks

        pass in channel name str i.e. 'ai0' or list of strings ['ai0', 'ai1', ...] for one of the arguments
        '''
        # create generic task
        self.task = nq.Task()

        # assign device name
        self.device_name = device

        # init analog in task
        if ai_channels is not None:
            self.__ai_init(ai_channels)
            
        # init analog out task
        elif ao_channels is not None:
            self.__ao_init(ao_channels)
            
        # init counter in task
        elif ci_channels is not None:
            pass

        # init counter out task
        elif co_channels is not None:
            pass

        # init digital in task
        elif di_channels is not None:
            pass

        # init digital out task
        elif do_channels is not None:
            pass
        
        # error message
        else:
            message = 'Pass in a string symbolizing a channel or list of strings for only one of parameters:\nai_channels, ao_channels, ci_channels, co_channels, di_channels, do_channels'
            title = 'Task Create Error!'
            msg.showerror(title, message)


 ## individual init for channel types ##

    def __ai_init(self, channels):
        
        # init single channel
        if isinstance(channels, str):
            # add channel
            self.task.ai_channels.add_ai_voltage_chan(self.device_name + '/' + channels)

            # create stream
            self.stream = in_stream.InStream(self.task)

            # create reader
            self.reader = stream_readers.AnalogSingleChannelReader(self.stream)

        # init multi channel
        elif isinstance(channels, list):
            # add channels
            for channel in channels:
                self.task.ai_channels.add_ai_voltage_chan(self.device_name + '/' + channel)
            
            # create stream
            self.stream = in_stream.InStream(self.task)

            # create reader
            self.reader = stream_readers.AnalogMultiChannelReader(self.stream)


    def __ao_init(self, channels):
        # init single channel
        if isinstance(channels, str):
            self.task.ao_channels.add_ao_voltage_chan(self.device_name + '/' + channels)

        # init multi channel
        elif isinstance(channels, list):
            for channel in channels:
                self.task.ao_channels.add_ao_voltage_chan(self.device_name + '/' + channel)


    def __ci_init(self, channels):
        pass


    def __co_init(self, channels):
        pass


    def __di_init(self, channels):
        pass

    
    def __do_init(self, channels):
        pass

    
 ## configuration functions ##

    def cfg_timing(self, rate, finite = True, samples = None):
        '''
        configure the timing for the task
        '''
        if finite:
            self.task.timing.cfg_samp_clk_timing(rate, sample_mode = AcquisitionType.FINITE)

if __name__ == "__main__":
    NQTask()

