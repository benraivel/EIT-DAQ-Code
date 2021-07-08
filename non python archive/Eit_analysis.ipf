#include <Strings as Lists>
#pragma rtGlobals=1        // Use modern global access method.

// given a folder of data, use smoothing/peak-finding to find an integer offset for each data set then average

// For the program below it is assumed that:
//  Channel 1:  Data
//  Channel 2:  Fabry Perot



Menu "Macros"
    
    "LoadSingleScopeData...", LoadSingleScopeData()
    "LoadAveragedScopeData...", LoadAveragedScopeData()
    "FPCalibrate...", FabryPerotCalibration()
    "FPCalibrateSmooth...", FabryPerotCalibration_Smooth()
End