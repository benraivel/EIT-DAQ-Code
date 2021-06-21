# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 14:33:43 2021

@author: bjraiv23
"""

import nidaqmx as nq
from nidaqmx import *


dev = nq.system.device.Device('NI_PCIe-6351')

print(dev.terminals)