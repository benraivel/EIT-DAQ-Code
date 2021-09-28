import numpy as np
import data
import EITAnalysis as an

import matplotlib.pyplot as plt
'''
A class to hold aggregated data once mapped on to frequency
    - stores an average value and a tally for each 'bin'
    - bin size given in MHz
    - 0 MHz at first fabry perot peak

'''
class DataBin:
    def __init__(self, range = 1000, bin_size = 0.1):
        # set data bin size
        self.bin_size = bin_size

        # compute length
        self.length = int(range/bin_size)
        self.data = np.empty(self.length)
        self.tally = np.zeros(self.length)
    
    def get_data(self):
        return (self.data, self.tally)

    def insert_set(self, data_set, mapping_polynomial):
        '''
        add data_set to self.data
        '''
        # for each point
        for i in range(len(data_set)):

            # if its location is >0MHz
            if mapping_polynomial(i) > 0:
                data_value = data_set[i]
                new_index = int(mapping_polynomial(i)/self.bin_size)

                # check if the current array can hold the value
                if new_index >= self.length:
                    self.expand_array(new_index)

                # if a value exists at the location:
                if self.tally[new_index] != 0:
                    
                    # compute total
                    total = self.data[new_index]*self.tally[new_index]

                    # increase by new value
                    new_total = total + data_value

                    # increment tally
                    self.tally[new_index] = self.tally[new_index] + 1

                    # compute new average value
                    self.data[new_index] = new_total/self.tally[new_index]

                # otherwise:
                else:
                    self.data[new_index] = data_value
                    self.tally[new_index] = 1

            
    def expand_array(self, new_length):
        '''
        appropriatley increase size of array
        '''
        self.length = new_length+1
        print('Expanded!')
        # create new data array (doubled size)
        temp_data = np.empty(self.length)

        # create new tally array (doubled size)
        temp_tally = np.zeros(self.length)

        # copy values over
        for i in range(len(self.data)):
            temp_data[i] = self.data[i]
            temp_tally[i] = self.tally[i]

        # re-assign
        self.data = temp_data
        self.tally = temp_tally

def main():

    # create DataBin object
    avg_dat = DataBin()

    all_data = []

    for i in range(10):

        print('loading run' + str(i) + '.csv:')
        filestr = 'testdata/set2/run' + str(i) + '.csv'
        # import data for testing
        test_data = data.Data(filestr)
        
        # select fabry perot data
        fabry_perot = test_data.select_dimension(1).T[0]
        print('max fp value:' + str(np.amax(fabry_perot)))

        # select data signal
        data_signal = test_data.select_dimension(0).T[0]

        all_data.append(data_signal)

        fit = an.fit_fabry_perot_peaks(fabry_perot, threshold=2)

        fit_poly = fit['poly']

        print('fit coeff:' + str(fit_poly.coef) + '\n\n')

        avg_dat.insert_set(data_signal, fit_poly)

        if i == 0:
            plt.subplot(311)
            plt.scatter(fit['freq_data'], data_signal, s = 1)

    all_data = np.array(all_data)

    avg = np.average(all_data, axis = 0)
    idx = np.arange(len(avg))

    freq = np.linspace(0, avg_dat.length*avg_dat.bin_size, avg_dat.length)
    plt.subplot(312)
    plt.scatter(freq, avg_dat.get_data()[0], s = 1)
    plt.subplot(313)
    plt.scatter(idx, avg, s = 1)
    plt.show()
    print(np.amax(avg_dat.get_data()[0]))
    print(np.amax(avg))

# main method for offline testing
if __name__ == "__main__":
    main()