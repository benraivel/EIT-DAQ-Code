import time
import subprocess
import logging
import warnings
import wolframclient
from wolframclient.language import wl, wlexpr
from wolframclient.evaluation import WolframLanguageSession

def terminate_kernels():
     print('terminating mathematica kernels')
     process = subprocess.run("killmathematica.cmd")
     print(process)
     
def get_fabry_perot(data):
    fp_waves = []
    for data_set in data:
        fp_waves.append(data_set[1])
    return fp_waves

def fabry_perot_get_peaks(data, smoothing, threshold):
    ''' 
    pass in array of 2D data sets
    returns indices of peaks that survive gaussian smoothing above threshold
    debug returns peak heights as well
    '''
    terminate_kernels()
    
    fp_data = get_fabry_perot(data)
    
    sets = len(fp_data)
    
    session = WolframLanguageSession()
    session.start(block = True)
    start_time = time.time()
    print('fabry_perot_get_peaks() session started')
    print('evaluating ' + str(sets) + ' fabry perot data sets')
    
    peak_data = []
    
    for fp_array in fp_data:
        peaks = session.evaluate(wl.Transpose(wl.FindPeaks(fp_array, smoothing, 0, threshold)))
        peak_data.append(list(peaks))
        
    elapsed_time = time.time() - start_time
    print('evaluation completed in ' + str(elapsed_time) + ' seconds' )
    session.stop()
    print('fabry_perot_get_peaks() session stopped')
    
    return peak_data

def generate_frequency_fit_data(data):
    freq_fit_data_set = []
    for peak_data in data:
        freq_fit_data = []
        for i in range(len(peak_data)):
            freq_fit_data.append([peak_data[0][i], 91.5*i])
        freq_fit_data_set.append(freq_fit_data)
    #print(freq_fit_data_set[0])

def fabry_perot_fit_frequency(data):
    freq_fit_data_set = generate_frequency_fit_data(peak_data_set)
    session = WolframLanguageSession()
    session.start(block = True)
    start_time = time.time()
    print('fabry_perot_fit_frequency() session started')
    print('evaluating ' + str(sets) + ' sets of data')
    
    fit_coefficients = []
    for freq_fit_data in freq_fit_data_set:
        fit = session.evaluate(wl.CoefficientList(wl.Fit(freq_fit_data, wlexpr('{1, x, x^2, x^3, x^4}'), wlexpr('{x}')), wlexpr('{x}')))
        fit_coefficients.append(fit)
    elapsed_time = time.time() - start_time
    print('evaluation completed in ' + str(elapsed_time) + ' seconds' )
    session.stop()
    print('fabry_perot_fit_frequency() session stopped')
    
    return fit











# hi