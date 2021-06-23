'''
Created on Wed Jun 23 09:18:41 2021

@author: bjraiv23

holds data analysis functions that use the wolfram python client
'''

# import wolfram packages
import wolframclient
from wolframclient.language import wl, wlexpr
from wolframclient.evaluation import WolframLanguageSession


def fabry_perot_get_peaks(fp_array, smoothing, threshold, debug = False):
    ''' 
    pass in 1-D array of fabry perot data
    returns indices of peaks that survive gaussian smoothing above threshold
    debug returns peak heights as well
    '''
    session = WolframLanguageSession()
    print('session started')
    print(fp_array)
    peaks = session.evaluate(wl.FindPeaks(fp_array, smoothing, 0, threshold))
    print(peaks)
    
    session.terminate()
    
    if debug:
        return peaks
    
    else:
        indices = []
        for peak in peaks:
            indices.append(peak[0])
        return indices


def fabry_perot_fit_frequency(indices):
    
    session = WolframLanguageSession()
    print('session started')
    freq_data = []
    
    for i in range(len(indices)):
        freq_data.append([indices[i], 91.5*i])
    
    print(freq_data)
    fit = session.evaluate(wl.CoefficientList(wl.Fit(freq_data, wlexpr('{1, x, x^2, x^3, x^4}')), wlexpr('{x}')))
    print(fit)
    session.terminate()
    
    return fit