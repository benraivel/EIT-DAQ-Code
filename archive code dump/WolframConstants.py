'''
enumerated constants for WolframSession
'''
# import modules
from enum import Enum
from wolframclient.language import wlexpr


## enumerated wlexpr() ##

class PlotRange(Enum):
    FULL = wlexpr('PlotRange -> Full')

class ImageSize(Enum):
    SMALL = wlexpr('ImageSize -> Small')
    MEDIUM = wlexpr('ImageSize -> Medium')
    LARGE = wlexpr('ImageSize -> Large')

class ImageResolution(Enum):
    NORMAL =  wlexpr('ImageResolution -> 72')
    HIGH = wlexpr('ImageResolution -> 200')