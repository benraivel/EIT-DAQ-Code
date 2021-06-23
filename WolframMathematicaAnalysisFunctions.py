'''
Created on Wed Jun 23 09:18:41 2021

@author: bjraiv23

holds data analysis functions that use the wolfram python client
'''

# import wolfram packages
import wolframclient as wc
from wolframclient.language import wl, wlexpr
from wolframclient.evaluation import WolframLanguageSession


def fabry_perot_get_peaks(fp_array, smoothing, threshold, debug = False):
    ''' 
    pass in 1-D array of fabry perot data
    returns indices of peaks with gaussian smoothing and 
    
    '''
    session = WolframLanguageSession()
    
    peaks = session.evaluate(wl.FindPeaks(fp_array, smoothing, 0, threshold))
    if debug:
        return peaks
    else:
        indices = []
        for peak in peaks:
            indices.append(peak[0])
        return indices


def fabry_perot_fit_frequency():
    pass