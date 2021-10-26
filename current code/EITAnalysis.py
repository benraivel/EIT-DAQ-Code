'''
replacing wolframsession with scipy
'''

import numpy as np
import pandas as pd
from PIL import Image, ImageTk
import time
from datetime import timedelta
import subprocess

import matplotlib.pyplot as plt

# get necessary scipy functions

from scipy.signal import find_peaks

def fit_fabry_perot_peaks(data, threshold, seperation = 1000, order = 5,  npeaks = None):
    '''
        given a 1D array of fabry perot data, threshold in volts, seperation in indices, and order:
        return dictionary
    '''
    if npeaks is not None:
        peaks = find_peaks(data, height = threshold, distance = len(data)/(2*npeaks))
    else:
        peaks = find_peaks(data, height = threshold, distance = seperation)
    
    num_found = len(peaks[0])

    heights = peaks[1]['peak_heights']

    # create 'points' necessary to fit
    peak_freq = np.arange(0, 91.5*num_found, 91.5)

    # create polynomial fit
    poly = np.polynomial.Polynomial.fit(peaks[0], peak_freq, order)

    #print(poly(1))

    # use polynomial linspace to get x axis data
    freq = poly.linspace(n =len(data), domain = [0, len(data)])[1]

    return {'poly' : poly, 'n' : num_found, 'peak_heights' : heights, 'freq_data' : freq}

 
def main():
    # import data for testing
    test_data = pd.read_csv('testdata/set1/run1.csv')
    
    # select fabry perot data
    fabry_perot = test_data.select_dimension(1).T[0]

    # select data signal
    data_signal = test_data.select_dimension(0).T[0]

    # get polynomial fit of fabry perot peaks
    freq = fit_fabry_perot_peaks(fabry_perot, 2, npeaks = 10)[1]

    print(np.ptp(freq))

    plt.plot(freq, data_signal)
    plt.show()


# main method for offline testing
if __name__ == "__main__":
    main()
    