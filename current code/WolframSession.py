''' 
creates a wolfram language session

methods use the session to run mathematica operations on python data

notes:
    - look closer at serializing and deserializing wxf
'''

# import wolfram client api modules
import wolframclient
from wolframclient.language import wl, wlexpr
from wolframclient.evaluation import WolframLanguageSession
from wolframclient.serializers import wolfram_encoder
from wolframclient.deserializers import WXFConsumerNumpy

# import other necessary modules
import numpy as np
from PIL import Image, ImageTk
import time
from datetime import timedelta
import subprocess

# scipy
from scipy.signal import find_peaks

# get wolfram constants
import WolframConstants as wc


class WolframSession():
    
    def __init__(self):
        ''' 
        create wolfram language session using numpy consumer
        
        wait for session start and record start time
        '''
        self.session = WolframLanguageSession(consumer = WXFConsumerNumpy)
        self.session.start(block = True)
        self.start_time = time.time()


    def end(self):
        ''' 
        ends session gracefully
        
        returns string with total time session was active
        '''
        self.end_time = time.time()
        self.session.stop()
        elapsed_time = timedelta(seconds = self.end_time - self.start_time)

        return 'Wolfram Language Client session finished \nTotal elapsed time: ' + str(elapsed_time)


    def __gen_freqdat(self, peaks):
        '''
        creates data for fit_fabryperot

        given a set of peak indicies return array: [[i0, 0], [i1, 91.5], ...]
        '''
        n = len(peaks)
        data = []
        
        for i in range(n):
            data.append([peaks[i], 91.5*i])
            
        return data


    def fit_fabryperot(self, fp_data, threshold_voltage = 2, min_seperation= 1000):
        '''
        finds peak indices with scipy

        peaks must excede threshold_voltage and be seperated by min_seperation indices from the next nearest peak in either direction

        return tuple: (quartic fit coefficients of data from gen_freqdat, peaks found by scipy)
        '''
        peaks = find_peaks(fp_data, height = threshold_voltage, distance = min_seperation)      
        data = self.__gen_freqdat(peaks[0])
        fit = self.session.evaluate(wl.CoefficientList(wl.Fit(data, wlexpr('{1, x, x^2, x^3, x^4}'), wlexpr('{x}')), wlexpr('{x}')))
        
        return (fit, peaks)


    def meanshift(self, data, r, d):
        '''
        filters data with MeanShiftFilter
        
        averages points in domain +-r and range +-d
        
        preserves significant edges while reducing noise
        '''
        return self.session.evaluate(wl.MeanShiftFilter(data, r, d))


    def resample(self, data, new_length, scheme = "Bin"):
        '''
        resamples data to new length using scheme
        '''
        return self.session.evaluate(wl.ArrayResample(data, new_length, scheme))


    def listplot(self, data, range = wc.PlotRange.FULL, size = wc.ImageSize.MEDIUM, resolution = wc.ImageResolution.HIGH):
        '''
        plot with Listplot with full range

        rasterize as a large image and get pixel data in array

        return tk compatible Image object
        '''
        plot_data = np.asarray(np.uint8(self.session.evaluate(wl.ImageData(wl.Image(wl.ListPlot(data, range), size, resolution))) * 255))

        return ImageTk.PhotoImage(Image.fromarray(plot_data))
    
    
    def def_function(self, name, arguments, definition):
        pass


    def __load_testdata(self, return_fp = True):
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


    

def terminate_kernels():
        ''' 
        kills all local mathematica/wolfram kernels, use carefully
        '''
        process = subprocess.run("C:\\Users\\bjraiv23\\Documents\\GitHub\\Python-Experiment-Control-Code\\utility\\killmathematica.cmd")
        return str(process)

