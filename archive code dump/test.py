import nidaqmx as nq
import numpy as np
from nidaqmx import *


with nq.system.device.Device() as Dev:
    

'''
with nq.Task() as freq_task:

    freq_task.ci_channels.add_ci_freq_chan('NI_PCIe-6351/ctr0')

    stream = nq._task_modules.in_stream.InStream(freq_task)
    reader = nq.stream_readers.CounterReader(stream)

    freq = np.empty(10, float)
    duty = np.empty(10, float)
    
    reader.read_many_sample_pulse_frequency(freq, duty, 10)

'''
