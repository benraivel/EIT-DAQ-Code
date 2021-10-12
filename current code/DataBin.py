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
        '''
        creates DataBin object to aggregate many sucessive sets of timeseries data
        
        '''
        # set data bin size
        self.bin_size = bin_size

        # compute length
        self.length = int(range/bin_size)

        # create arrays to hold data
        self.data = np.empty(self.length)
        self.tally = np.zeros(self.length)
    
    def get_data(self):
        '''
        returns tuple: (data, tally)
        '''
        return (self.data, self.tally)

    def insert_set(self, data_set, mapping_polynomial):
        '''
        add data_set to self.data using mapping_polynomial to find the index at which to insert each point
        '''
        # determine the max index value this set will produce
        max = mapping_polynomial(len(data_set))

        # if it is greater than the current arrays can hold, expand them
        if max > self.length:
            self.expand_array(max)

        # for each point
        for i in range(len(data_set)):

            # if it maps to >0MHz
            if mapping_polynomial(i) > 0:
                data_value = data_set[i]
                new_index = int(mapping_polynomial(i)/self.bin_size)

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

                # otherwise add the new value and set the tally to one
                else:
                    self.data[new_index] = data_value
                    self.tally[new_index] = 1

            
    def expand_array(self, newlength):
        '''
        increase the size of the array to newlength
        '''
        # create new data array (doubled size)
        temp_data = np.empty(newlength)

        # create new tally array (doubled size)
        temp_tally = np.zeros(newlength)

        # copy values over
        for i in range(len(self.data)):
            temp_data[i] = self.data[i]
            temp_tally[i] = self.tally[i]

        # re-assign
        self.data = temp_data
        self.tally = temp_tally
        self.length = newlength

def main():

    # create DataBin object
    avg_dat = DataBin()

    for i in range(10):

        print('loading run' + str(i) + '.csv:')
        filestr = 'testdata/set4/run' + str(i) + '.csv'
        # import data for testing
        test_data = data.Data(filestr)
        
        # select fabry perot data
        fabry_perot = test_data.select_dimension(1).T[0]
        print('max fp value:' + str(np.amax(fabry_perot)))

        # select data signal
        data_signal = test_data.select_dimension(0).T[0]

        fit = an.fit_fabry_perot_peaks(fabry_perot, threshold=2)

        fit_poly = fit['poly']

        print('fit coeff:' + str(fit_poly.coef))

        avg_dat.insert_set(data_signal, fit_poly)

        if i ==9:
            plt.scatter(fit['freq_data'], data_signal, s = 1)
            plt.show()

    freq = np.linspace(0, avg_dat.length*avg_dat.bin_size, avg_dat.length)
    plt.scatter(freq, avg_dat.get_data()[0], s= 1)
    plt.show()

# main method for offline testing
if __name__ == "__main__":
    main()