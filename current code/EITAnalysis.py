'''
replacing wolframsession with scipy
'''

import numpy as np
from PIL import Image, ImageTk
import time
from datetime import timedelta
import subprocess
import data

import matplotlib.pyplot as plt

# get necessary scipy functions

from scipy.signal import find_peaks

def fit_fabry_perot_peaks(data, threshold, seperation = 1000, order = 5,  npeaks = None):
    '''
        given a 1D array of fabry perot data, threshold in volts, seperation in indices, and order:
        return list of coefficients for polynomial of degree order mapping index to MHz
    '''
    if npeaks is not None:
        peaks = find_peaks(data, height = threshold, distance = len(data)/(2*npeaks))
    else:
        peaks = find_peaks(data, height = threshold, distance = seperation)
    

    freq = np.arange(0, 91.5*len(peaks[0]), 91.5)

    return np.polynomial.Polynomial.fit(peaks[0], freq, order)
    
def main():
    # import data for testing
    test_data = data.Data('testdata/run0.csv')
    
    # select fabry perot data
    fabry_perot = test_data.select_data('fp').T[0]

    # select data signal
    data_signal = test_data.select_data('data').T[0]

    # get polynomial fit of fabry perot peaks
    poly = fit_fabry_perot_peaks(fabry_perot, 2, npeaks = 10)

    # use polynomial linspace to get x axis data
    freq = poly.linspace(n =len(fabry_perot), domain = [0, len(fabry_perot)])[1]

    plt.plot(freq, data_signal)
    plt.show()


# main method for offline testing
if __name__ == "__main__":
    main()
    