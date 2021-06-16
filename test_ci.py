import nidaqmx

with nidaqmx.Task() as task:
    task.ci_channels.add_ci_freq_chan('NI_PCIe-6351/ctr0')

    print('1 Channel 1 Sample Read: ')
    data = task.read()
    print(data)

    print('1 Channel N Samples Read: ')
    data = task.read(number_of_samples_per_channel=8)
    print(data)
