import nidaqmx
import math
import numpy as np
from nidaqmx import *
import matplotlib.pyplot as plt
import settings
from multiprocessing import Process


# this script defines various waveforms and controls for PCI-6733

def gaussian(amp, tail, duration, rate):
    # starting out 3 stdevs away from mean
    # tail: how many stdevs away
    # duration: how long one cycle is

    mu = 0
    var = 1
    global time_step
    global default_rate
    default_rate = rate
    time_step = 1/rate

    steps = int(duration/time_step)
    x = mu - tail*math.sqrt(var)
    gauss = np.array([])

    for i in range(-int(steps/2),int(steps/2)):
        x = x + 2*tail*math.sqrt(var)/steps
        # g = (1/math.sqrt(2*math.pi*var)) * np.exp(-( (x-mu)**2 / ( 2.0 * var ) ) )
        g = amp * np.exp(- (x - mu)**2/(2.0*var))
        gauss = np.append(gauss, np.float16(g))
    return gauss

def sin(amp, freq_scale, duration, rate):
    # amp: amplitude
    # freq_scale: relative frequency compared to 1.
    # duration: period

    global time_step
    global default_rate
    default_rate = rate
    time_step = 1/rate

    steps = int(duration/time_step)
    sx = np.array([])
    for i in range(-int(steps/2),int(steps/2)):
        # from -Pi to Pi
        val = amp*math.sin(2*math.pi*i*freq_scale/steps)
        sx = np.append(sx, np.float16(val))

    return sx

def sinc(amp, duration, rate):
    # amp: amplitude of max

    global time_step
    global default_rate
    default_rate = rate
    time_step = 1/rate

    critical_x = 30
    steps = int(duration/time_step)
    s = np.array([])
    for i in range(-int(steps/2),int(steps/2)):
        if i == 0:
            val = 1.0*amp
        else:
            val = amp*math.sin(critical_x*i/steps)/(critical_x*i/steps)
        s = np.append(s, np.float16(val))
    return s

def sawtooth(amp, duration, rate):
    # amp: amplitude of max

    global time_step
    global default_rate
    default_rate = rate
    time_step = 1/rate

    steps = int(duration/time_step)
    t = np.array([])
    for i in range(-int(steps/2),int(steps/2)):
        val = amp*i/steps
        t = np.append(t, np.float16(val))

    print('Number of time points: ', len(t))
    return t

def set_voltage(volt, duration_on, duration, rate):
    # set a voltage for a number of points
    # makes a square pulse for some num_points
    # then turns to zero for num_points zero

    global time_step
    global default_rate
    default_rate = rate
    time_step = 1/rate

    voltage = np.array([])

    # print('First number:', int(duration_on/time_step))
    # print('Second number:', int((duration - duration_on)/time_step))

    for i in range(int(duration_on*rate)):
        voltage = np.append(voltage, np.float16(volt))
    if duration != duration_on:
        for i in range(int((duration - duration_on)*rate)):
            voltage = np.append(voltage, np.float16(0.0))

    return voltage

def test_set_digital(digit, duration_on, duration, rate):
    # set a voltage for a number of points
    # makes a square pulse for some num_points
    # then turns to zero for num_points zero
    # returns an array of uint8 integers

    global time_step
    global default_rate
    default_rate = rate
    time_step = 1/rate

    out = np.array([])
    out_int_8 = np.array([])
    for i in range(int(duration_on/time_step)+1):
        out = np.append(out, digit)
    for i in range(int((duration - duration_on)/time_step)):
        out = np.append(out, 1)
    out_int_8 = np.array(out, dtype = np.uint8)
    # print('Num points: ', len(out))
    return out_int_8

def set_digital(digit, duration_on, duration, rate):
    # set a voltage for a number of points
    # makes a square pulse for some num_points
    # then turns to zero for num_points zero
    # returns an array of integers, regular integers

    global time_step
    global default_rate
    default_rate = rate
    time_step = 1/rate

    out = np.array([])
    out_int_8 = np.array([])
    for i in range(int(duration_on*rate)):
        out = np.append(out, digit)
    if duration != duration_on:
        for i in range(int((duration - duration_on)*rate)):
            out = np.append(out, 1)
    out_int_8 = np.array(out, dtype = np.uint8)
    # print('Num points: ', len(out))
    return out_int_8

def to_digit(switch, rate):
    # switch has the form [[state_number, delay]]
    # which characterizes the status of each digital output
    # for that time frame
    # the rate specifies how many numbers should be generated in the end
    events = len(switch) # the number of events is the len() of switch
    digits = np.array([])
    for e in range(events):
        digits = np.concatenate((digits, set_digital(switch[e][0], switch[e][1], switch[e][1], rate)))

    # now convert to uint8
    digits = np.array(digits, dtype=np.uint8)
    # print(digits)
    return digits

def set_to_zero(duration, rate):
    # creates an array of zeros to 0 volts

    global time_step
    global default_rate
    default_rate = rate
    time_step = 1/rate

    voltage = np.array([])
    for i in range(int(duration/time_step)):
        voltage = np.append(voltage, np.float16(0.0))
    return voltage

def set_delay(duration, wave, rate):
    # create a delay between signal beginnings
    # by replacing the first `steps' values by zeros

    global time_step
    global default_rate
    default_rate = rate
    time_step = 1/rate
    zeros = np.array([])
    # new_wave = np.copy(wave)

    if int(duration/time_step) > len(wave):
        return set_to_zero(len(wave))

    for i in range(int(duration/time_step)):
        zeros = np.append(zeros, np.float16(0.0))

    delay = np.concatenate((zeros, wave))
    delay = delay[0:len(wave)]
    return delay

def lin_ramp(volt_start, volt_end, duration, rate):
    # generates a linear ramp
    # return a np.array()
    global time_step
    global default_rate
    default_rate = rate
    time_step = 1/rate

    steps = int(duration*rate)
    volt = np.array([])
    for i in range(-int(steps/2),int(steps/2)):
        val = (volt_end + volt_start)/2 + (volt_end - volt_start)*i/steps
        volt = np.append(volt, np.float16(val))

    return volt

def sin_ramp(volt_start, volt_end, duration, rate):
    # generates a linear ramp
    # return a np.array()
    global time_step
    global default_rate
    default_rate = rate
    time_step = 1/rate

    steps = int(duration*rate)
    volt = np.array([])
    for i in range(-int(steps/2),int(steps/2)):
        val = (volt_start + volt_end)/2 +  (volt_end - volt_start)*math.sin(math.pi*i/steps)/2
        volt = np.append(volt, np.float16(val))

    # print('Number of time points: ', len(t))
    return volt

def exp_ramp(volt_start, volt_end, duration, rate, time_constant):
    # generates a linear ramp
    # return a np.array()
    global time_step
    global default_rate
    default_rate = rate
    time_step = 1/rate

    steps = int(duration*rate)
    volt = np.array([])
    for i in range(-int(steps/2),int(steps/2)):
        val = volt_start +  (volt_end - volt_start)*(1 - math.exp(-(1/time_constant)*(i + int(steps/2))/int(steps)))
        volt = np.append(volt, np.float16(val))

    # print('Number of time points: ', len(t))
    return volt

def to_wave(instruction, rate):
    # this function takes in instructions
    # and returns a waveform
    events = len(instruction)
    wave = np.array([])
    for e in range(events):
        mode = instruction[e][0]
        duration = instruction[e][1]
        # step = instruction[e][2]
        volts = instruction[e][2]

        if mode == '-Select-': # if no ramping, do the same as before
            wave = np.concatenate((wave, set_voltage(volts, duration, duration, rate)))
        elif mode == 'Lin. Ramp':
            if e == 0 or e == events-1:
                volt_start = 0
                volt_end = instruction[e][2]
                wave = np.concatenate((wave, lin_ramp(volt_start, volt_end, duration, rate)))
            else:
                # if things are okay then collect the end points:
                volt_start = instruction[e-1][2]
                volt_end = instruction[e][2]
                wave = np.concatenate((wave, lin_ramp(volt_start, volt_end, duration, rate)))

        elif mode == 'Sin. Ramp':
            if e == 0 or e == events-1:
                volt_start = 0
                volt_end = instruction[e][2]
                wave = np.concatenate((wave, sin_ramp(volt_start, volt_end, duration, rate)))
            else:
                # if things are okay then collect the end points:
                volt_start = instruction[e-1][2]
                volt_end = instruction[e][2]
                wave = np.concatenate((wave, sin_ramp(volt_start, volt_end, duration, rate)))

        elif mode == 'Exp. Ramp':
            if e == 0 or e == events-1:
                volt_start= 0
                volt_end = instruction[e][2]
                time_constant = instruction[e][2]
                wave = np.concatenate((wave, exp_ramp(volt_start, volt_end, duration, rate, math.sqrt(duration) ) ) )
            else:
                # if things are okay then collect the end points:
                volt_start = instruction[e-1][2]
                volt_end = instruction[e][2]
                wave = np.concatenate((wave, exp_ramp(volt_start, volt_end, duration, rate, math.sqrt(duration) ) ) )

    return wave

def digital_wave_to_analog(wave):
    # this function converts the 1D array sent to the digital channels
    # into 8 1D analog arrays, just for plotting purposes.


    # initializing step
    w = list(format(list(wave)[0], '08b')) # turns 8 bit unsigned int to list of 0 and 1
    t = [] # this is just a buffer
    for i in range(settings.digital_channels):
        t.append([w[i]])
    output_wave = np.array(t) # initializing the array


    for element in range(1, len(wave)):
        w = list(format(list(wave)[element], '08b')) # turns 8 bit unsigned int to list of 0 and 1
        tt = [] # this is also a buffer
        for i in range(settings.digital_channels): # 8 is the number of digital channels
            tt.append([w[i]])
        output_wave = np.append(output_wave, tt, axis = 1) # append this way, NOT concatenatinng

    return output_wave

def simulate(cycles, rate, wave1=np.array([np.float16(0.0)]*100),
                               wave2=np.array([np.float16(0.0)]*100),
                               wave3=np.array([np.float16(0.0)]*100),
                               wave4=np.array([np.float16(0.0)]*100),
                               wave5=np.array([np.float16(0.0)]*100),
                               wave6=np.array([np.float16(0.0)]*100),
                               digit=np.array([np.float16(0.0)]*100)
                               ):
    # this function takes in the data and plots the procedure

    global time_step
    global default_rate
    default_rate = rate
    time_step = 1/rate
    time = []
    t = 0
    for cycle in range(cycles):
        for w in range(len(wave1)):
            time.append(t)
            t = t + time_step
    wave1 = np.tile(wave1, cycles)
    wave2 = np.tile(wave2, cycles)
    wave3 = np.tile(wave3, cycles)
    wave4 = np.tile(wave4, cycles)
    wave5 = np.tile(wave5, cycles)
    wave6 = np.tile(wave6, cycles)
    digit = digital_wave_to_analog(digit) # transforms to binary
    digit = np.tile(digit, cycles)
    print('Data dimension: ', len(time))

    fig, axs = plt.subplots(2)
    fig.suptitle('Experimental Procedure')
    axs[0].plot(time, wave1, time, wave2, time, wave3, time, wave4, time, wave5, time, wave6)
    axs[0].set(ylabel='Analog (V)')
    axs[1].plot(time, digit[7], time, digit[6], time, digit[5], time, digit[4], time, digit[3], time, digit[2], time, digit[1], time, digit[0])
    axs[1].set(ylabel='Digital (On/OFF)')
    plt.show(block=False)
    print('--- Plot graph finish ---')

    # plt.show()
    return

def run(iter, rate, wave1, wave2, wave3, wave4, wave5, wave6, digits):

    global Sample_Per_Chan
    Sample_Per_Chan = 10

    global time_step
    global default_rate
    default_rate = rate
    time_step = 1/rate
    global data_dimension
    data_dimension = len(wave1)

    task_ao = nidaqmx.Task()
    task_do = nidaqmx.Task()
    # analog channels
    ao_0 = task_ao.ao_channels.add_ao_voltage_chan('Dev2/ao0')
    ao_1 = task_ao.ao_channels.add_ao_voltage_chan('Dev2/ao1')
    # ao_2 = task_ao.ao_channels.add_ao_voltage_chan('Dev2/ao2')
    # ao_3 = task_ao.ao_channels.add_ao_voltage_chan('Dev2/ao3')
    # ao_4 = task_ao.ao_channels.add_ao_voltage_chan('Dev2/ao4')
    # ao_5 = task_ao.ao_channels.add_ao_voltage_chan('Dev2/ao5')

    ao_0.ao_data_xfer_mech = nidaqmx.constants.DataTransferActiveTransferMode.DMA
    ao_1.ao_data_xfer_mech = nidaqmx.constants.DataTransferActiveTransferMode.DMA
    # ao_2.ao_data_xfer_mech = nidaqmx.constants.DataTransferActiveTransferMode.DMA
    # ao_3.ao_data_xfer_mech = nidaqmx.constants.DataTransferActiveTransferMode.DMA
    # ao_4.ao_data_xfer_mech = nidaqmx.constants.DataTransferActiveTransferMode.DMA
    # ao_5.ao_data_xfer_mech = nidaqmx.constants.DataTransferActiveTransferMode.DMA

    # digital channels
    # task_do.do_channels.add_do_chan('Dev2/port0/line0:7', line_grouping=nidaqmx.constants.LineGrouping.CHAN_FOR_ALL_LINES)
    # timing for DO
    # note that we want to get this started BEFORE the AO
    # task_do.timing.cfg_samp_clk_timing(rate= default_rate,
                                    # source = '/Dev2/ao/SampleClock',
                                    # sample_mode= nidaqmx.constants.AcquisitionType.CONTINUOUS,
                                    # samps_per_chan=Sample_Per_Chan)

    # continuous/finite mode for analog channels
    if iter == 'cont': # continuous mode
        task_ao.timing.cfg_samp_clk_timing(rate= default_rate,
                                    sample_mode= nidaqmx.constants.AcquisitionType.CONTINUOUS,
                                    samps_per_chan=Sample_Per_Chan)

    elif int(iter) == 1:
        print('The minimum value is 2.')
        task_do.stop()
        task_ao.stop()
        task_do.close()
        task_ao.close()
        exit()
    else:
        iterations = int(iter)
        task_ao.timing.cfg_samp_clk_timing(rate= default_rate,
                                    sample_mode= nidaqmx.constants.AcquisitionType.FINITE,
                                    samps_per_chan=data_dimension*iterations)


    test_Writer_ao = nidaqmx.stream_writers.AnalogMultiChannelWriter(task_ao.out_stream, auto_start=True)
    test_Writer_do = nidaqmx.stream_writers.DigitalSingleChannelWriter(task_do.out_stream, auto_start=True)
    input_wave = np.array([wave1,
                           wave2
                           #wave3,
                           #wave4,
                           #wave5,
                           #wave6
                           ])
    # IMPORTANT: do starts before ao
    # test_Writer_do.write_many_sample_port_byte(digits)
    test_Writer_ao.write_many_sample(input_wave)
    print('Running...')

    while True:
        settings.event, settings.values = settings.window.Read()
        if settings.event is None:
            break
        if settings.event == 'STOP' or iter != 'cont':
            # task.stop()
            # stop, then re-set everything to zero
            # test_Writer.write_many_sample([wave1*0, wave2*0, wave3*0, wave4*0]
            print(settings.event)
            task_do.stop()
            task_ao.stop()
            task_do.close()
            task_ao.close()
            return

def test_digital():
    task_ao = nidaqmx.Task()
    task_do = nidaqmx.Task()

    # pulser channel

    # analog channel
    task_ao.ao_channels.add_ao_voltage_chan('Dev1/ao0')
    # digital channels
    task_do.do_channels.add_do_chan('Dev1/port0/line0:7', line_grouping=nidaqmx.constants.LineGrouping.CHAN_FOR_ALL_LINES)

    # timing for DO
    # note that we want to get this started BEFORE the AO
    task_do.timing.cfg_samp_clk_timing(rate= 1e5,
                                    source = '/Dev1/ao/SampleClock',
                                    sample_mode= nidaqmx.constants.AcquisitionType.CONTINUOUS,
                                    samps_per_chan=1)
    # timing for AO
    task_ao.timing.cfg_samp_clk_timing(rate= 1e5,
                                    #source='/Dev1/ao/SampleClock',
                                    sample_mode= nidaqmx.constants.AcquisitionType.CONTINUOUS,
                                    samps_per_chan=1)

    test_Writer_ao = nidaqmx.stream_writers.AnalogSingleChannelWriter(task_ao.out_stream, auto_start=True)
    test_Writer_do = nidaqmx.stream_writers.DigitalSingleChannelWriter(task_do.out_stream, auto_start=True)
    wave_ao = sawtooth(1.0, 0.001, 1e5)
    wave_do = test_set_digital(4, 0.0008, 0.001, 1e5)
    test_Writer_do.write_many_sample_port_byte(wave_do)
    test_Writer_ao.write_many_sample(wave_ao)
    a = input('Press Enter to end: ')
    task_ao.close()
    task_do.close()

if __name__ == "__main__":
    test_digital()
