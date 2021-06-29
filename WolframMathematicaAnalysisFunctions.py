import time
import subprocess
import logging
import warnings
import wolframclient
from wolframclient.language import wl, wlexpr
from wolframclient.evaluation import WolframLanguageSession

'''
fit = session.evaluate(wl.CoefficientList(wl.Fit(freq_fit_data, wlexpr('{1, x, x^2, x^3, x^4}'), wlexpr('{x}')), wlexpr('{x}')))
'''

     
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

    










# hi