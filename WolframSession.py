''' 
create one off evaluator pool to run constantly during experiment
'''


import time
import subprocess
import logging
import warnings

import wolframclient
from wolframclient.language import wl, wlexpr
from wolframclient.evaluation import WolframLanguageAsyncSession, WolframEvaluatorPool


class WolframSession():
    
    def __init__(self):
        self.session = WolframLanguageAsyncSession()
        self.session.start(block = True)
        self.start_time = time.time()
        
    def session(self):
        return self.session

    def end_session(self):
        self.end_time = time.time()
        self.session.stop()
        elapsed_str = time.strftime('%H:%M:%S', self.end_time - self.start_time)
        return 'Wolfram Language Client session finished \ntotal elapsed time: ' + elapsed_str
    
def terminate_kernels():
    ''' 
    kills all local mathematica/wolfram kernels, use carefully
    '''
    process = subprocess.run("killmathematica.cmd")
    return str(process)