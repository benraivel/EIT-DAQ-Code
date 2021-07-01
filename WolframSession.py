''' 
creates a wolfram language session

methods use the session to run mathematica operations on python data
'''

# import wolfram client api modules
import wolframclient
from wolframclient.language import wl, wlexpr
from wolframclient.evaluation import WolframLanguageSession

# import other necessary modules
import time
from datetime import timedelta
import subprocess
import logging
import warnings


class WolframSession():
    
    def __init__(self):
        ''' 
        create wolfram language session, wait for start, record start time
        '''
        self.session = WolframLanguageSession()
        self.session.start(block = True)
        self.start_time = time.time()



    def end_session(self):
        ''' 
        ends session gracefully, returns string with total time session was active
        '''
        self.end_time = time.time()
        self.session.stop()
        elapsed_time = timedelta(seconds = self.end_time - self.start_time)
        return 'Wolfram Language Client session finished \nTotal elapsed time: ' + str(elapsed_time)


    
    def find_fabry_perot_peaks(self, fp_array, smoothing = 80, threshold = 3):
        '''
        given a 1D array of fabry perot data:
            - find peaks using smoothing and threshold
            - return array of indices only
        '''
        peak_index_data = []
        peaks = self.session.evaluate(wl.Transpose(wl.FindPeaks(fp_array, smoothing, 0, threshold)))
        indices = peaks[0]
        for index in indices:
            try:
                peak_index_data.append(int(index))
            except:
                peak_index_data.append(int(index[0]/index[1]))
        
        return peak_index_data


    
    def fit_fabry_perot_peaks(self, fp_array):
        '''
        given a 1D array of fabry perot data:
            - find peak indices with find_fabry_perot_peaks()
            - generate frequency 'data'
            - return coefficients of quartic fit
        '''
        peaks = self.find_fabry_perot_peaks(fp_array)       
        data = self.generate_frequency_data(peaks)        
        fit = self.session.evaluate(wl.CoefficientList(wl.Fit(data, wlexpr('{1, x, x^2, x^3, x^4}'), wlexpr('{x}')), wlexpr('{x}')))
        
        return fit


        
    def generate_frequency_data(self, peaks):
        
        npeak = len(peaks)
        
        freq_data = []
        
        for i in range(npeak):
            freq_data.append([peaks[i], 91.5*i])
            
        return freq_data
        
        



def terminate_kernels():
    ''' 
    kills all local mathematica/wolfram kernels, use carefully
    '''
    process = subprocess.run("killmathematica.cmd")
    return str(process)



def load_data_for_test(return_fp = True):
    '''
    use for developing wolfram functions without needing to gather data
    
    call with return_fp = False to get [[difference data], [fabry perot]]
    
    otherwise returns 1D array of fabry perot data
    '''
    # open known, existing, data file
    file = open('C:\\Users\\bjraiv23\\Desktop\\Experimental-Data\\Thu Jul 1, 2021\\12 10 27\\run0.csv', 'r')
    
    # create arrays to hold data once loaded
    difference_data = []
    fabry_perot_data = []
    
    # read first line into array
    line_array = file.readline().split(',')

    # for whole file:
    while len(line_array) == 2:
        difference_data.append(float(line_array[0]))
        fabry_perot_data.append(float(line_array[1]))
        line_array = file.readline().split(',')
        
    if return_fp:
        return fabry_perot_data
    else:
        return [difference_data, fabry_perot_data]


if __name__ == "__main__":
    
    test_array = load_data_for_test()
    
    test_session = WolframSession()
    
    peaks = test_session.find_fabry_perot_peaks(test_array)
    
    print(test_session.generate_frequency_data(peaks))
    
    print(test_session.fit_fabry_perot_peaks(test_array))
    
    print(test_session.end_session())







#