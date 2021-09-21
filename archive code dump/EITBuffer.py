'''
class that holds data and other stuff corresponding to one experiment
'''

import numpy as np

import WolframSession as ws
import WolframConstants as wc


class EITBuffer():

    def __init__(self, peaks, start = 0, step = 0.1):
        
        self.end = (peaks - 1) * 91.5 
        self.buffersize = (self.end - start)/step
        self.buffer = np.empty(self.buffersize)
        self.session = ws.WolframSession()

    def add(self, data, fabryperot):
        self.session.meanshift(fabryperot, )
