
# import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# import analysis functions
from EITAnalysis import fit_fabry_perot_peaks

class DataBin:
    '''
    Maps data into agregated array based on fabry perot fit
        - stores an average value and a tally for each 'bin'
        - bin size given in MHz
        - 0 MHz at first fabry perot peak
    '''

    def __init__(self, range = 1000, bin_size = 0.1):
        '''
        creates DataBin object to aggregate many sucessive sets of timeseries data
        
        '''
        # init number of sets
        self.num_sets = 0

        # set data bin size
        self.bin_size = bin_size

        # compute length
        self.arr_length = int(range/bin_size)

        # create arrays to hold data and tally
        self.data = np.empty(self.arr_length)
        self.tally = np.zeros(self.arr_length)
    
    def __str__(self):
        '''
        return string representation of DataBin object
        '''
        return 'DataBin object:\n\tnumber of data sets: ' + str(self.num_sets) + '\n\tnumber of bins: ' + str(self.length)

    def get_data(self):
        '''
        returns tuple: (data, tally)
        '''
        return (self.data, self.tally)

    def insert_set(self, new_set, mapping_polynomial):
        '''
        adds data_set to self.data
        
        uses mapping_polynomial to find the index at which to insert each point
        '''
        # determine the max index value this set will produce
        max = mapping_polynomial(len(new_set))

        # if it is greater than the current array length expand them appropriatley 
        if max > self.arr_length:
            self.expand_array(max)

        # for each point
        for i in range(len(new_set)):

            # if it maps to >0MHz
            if mapping_polynomial(i) > 0:
                new_value = new_set[i]
                new_index = int(mapping_polynomial(i)/self.bin_size)

                # if a value exists at the location:
                if self.tally[new_index] != 0:
                    
                    # compute current total
                    curr_total = self.data[new_index]*self.tally[new_index]

                    # increase by new value
                    new_total = curr_total + new_value

                    # increment tally
                    self.tally[new_index] = self.tally[new_index] + 1

                    # compute new average value
                    self.data[new_index] = new_total/self.tally[new_index]

                # otherwise add the new value and set the tally to one
                else:
                    self.data[new_index] = new_value
                    self.tally[new_index] = 1
        
        # increment set counter
        self.num_sets += 1

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

# class test functions:
def main():

    # create DataBin object
    avg_dat = DataBin()

    # create array for normal average
    all_data = []

    # for each data set in the folder
    for i in range(10):

        print('loading run' + str(i) + '.csv:')

        # update file to read
        filestr = 'testdata/set4/run' + str(i) + '.csv'

        # import data for testing
        test_data = pd.read_csv(filestr)
        
        # select fabry perot data
        fabry_perot = test_data.iloc[:,1]
        print('max fp value:' + str(np.amax(fabry_perot)))

        # select data signal
        data_signal = test_data.iloc[:,0]

        # add to normal average array
        all_data.append(data_signal)

        # get fit from fabry perot
        fit = fit_fabry_perot_peaks(fabry_perot, threshold=2)

        # get polynomial of fit
        fit_poly = fit['poly']

        print('fit coeff:' + str(fit_poly.coef.round(2)) + '\n\n')

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
    print(avg_dat)

if __name__ == "__main__":
    main()