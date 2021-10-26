'''
when run main(iter, samp_rate) is called with parameters:
    iter = 10
    samp_rate = 100,000 Hz
    
records iter sets of data at samp_rate for channels:
    'ai0' : difference signal
    'ai1' : fabry perot signal
    
data is saved as a series of .csv files at C:\\Users\\bjraiv23\\Desktop\\Experimental-Data\\[CURRENT DATE]\\[HH MM SS]
'ai0' is the 1st column etc.

modify last line of the file to change number of data sets collected or sampling frequency
'''
# import NI python API 
import nidaqmx as nq
from nidaqmx import *

# import necessary nidaqmx constants
from nidaqmx.constants import AcquisitionType

# import analysis functions
from EITAnalysis import fit_fabry_perot_peaks                                                                                                                                       

# import other modules
import numpy as np
import os
import time


def meas_ramp_time():
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
    
    return time_sec

def task_init(samp_rate, time):
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

def create_array(iterations, channels, samp_rate, time):
    '''
    creates array of 2D arrays in memory to hold experimental data
    
    pass in iterations, number of analog channels, sampling rate (Hz), and ramp time (s)
    
    returns data array (L*M*N where L <= iterations, M <= channels, and N <= samp_rate * time)
    '''
    return np.empty(iterations, channels, samp_rate*time)
    
def average_data(data):
    '''
    find a basic average
    '''

def save_data(data):
    '''
    pass in list of 2D numpy arrays with data
    
    - creates a folder if one does not exist at:
        C:\\Users\\bjraiv23\\Desktop\\Experimental-Data
    
    - creates a folder for the current day if one does not exist at:
        C:\\Users\\bjraiv23\\Desktop\\Experimental-Data\\[Weekday] [Month] [DD:YYYY]
        
    - creates a folder for the current experiment at:
        C:\\Users\\bjraiv23\\Desktop\\Experimental-Data\\[Weekday] [Month] [DD:YYYY]\\HH MM SS

    data is saved as series of csv files in experiment folder
    '''
    # get and format date and time information
    date_time = time.ctime().split()
    day = date_time[0] + ' ' + date_time[1] + ' ' + date_time[2] + ', ' + date_time[4]
    current_time = date_time[3].split(':')[0] + ' ' + date_time[3].split(':')[1] + ' ' + date_time[3].split(':')[2]
    
    # try to create directories, pass if they already exist
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
    
    # loop for each iteration/dataset in the list and write all points as lines in csv
    for i in range(len(data)):
        
        file = open('C:\\Users\\bjraiv23\\Desktop\\Experimental-Data\\' + day + '\\' + current_time + '\\run' + str(i) + '.csv', 'w')
        
        for j in range(len(data[0][0])):
            file.write(str(data[i][0][j]) + ', ' + str(data[i][1][j]) +'\n')
            
        file.close()

def main(iterations, samp_rate):
    ''' 
    performs basic experimental process by calling other functions in file in sucession
    '''
    # measure ramp time
    time = meas_ramp_time()
    
    # print message
    print('Ramp Time: ' + str(time) + ' seconds')
    
    # initialize task and configurations
    stream_reader = task_init(samp_rate, time)
    
    # create data array
    data = create_array(iterations, 2, samp_rate, time)
    
    # print message
    print('collecting ' + str(iterations) + ' sets of data') 
    
    # loop for iterations 
    for array in data:
        stream_reader.read_many_sample(array)
        
    #averages = average_data(data)
    
    #print(averages)
    
    #peaks = analyze_all(data)
    
    #print(peaks)
    
    #print(analyze_peak_seperations(peaks))
    # write data to file
    save_data(data)

# file test function
def test_func():
    arr = create_array(100, 3, 10000, 0.5)
    print(arr.shape)

# file main method call
if __name__ == "__main__":
    #main(10, 500000)
    test_func()
