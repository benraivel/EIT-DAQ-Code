#include <Strings as Lists>
#pragma rtGlobals=1		// Use modern global access method.
// This set of Functions will load data saved from a Textronix DP02024
// The data is stored in different formats depending on if the traces are acquired with or withouth averaging

// For the program below it is assumed that:
//  Channel 1:  Ramp
//  Channel 2:  Fabry Perot
//  Channel 3:  Signal
//  Channel 4:  Signal - Reference

// Note that a fifth channel would be needed to record the reference signal (or we could skip the ramp)

Menu "Macros"
	
	"LoadSingleScopeData...", LoadSingleScopeData()
	"LoadAveragedScopeData...", LoadAveragedScopeData()
	"FPCalibrate...", FabryPerotCalibration()
	"FPCalibrateSmooth...", FabryPerotCalibration_Smooth()
End

Function LoadAveragedScopeData()
// When averaging the scope outputs one column per trace
// This function assumes that all four traces are saved

String pathName
String filename
String w0, w1, w2, w3, w4
String GraphName0, GraphName1,GraphName2,GraphName3
String  GraphTitle0,GraphTitle1,GraphTitle2,GraphTitle3

String filename_ScopeTime = "T0000_ScopeTime"
String filename_Frequency = "T0000_Frequency"
String filename_Ramp = "T0000_Ramp"
String filename_FabryPerot = "T0000_FabryPerot"
String filename_ProbeSignal = "T0000_ProbeSignal"
String filename_DifferenceSignal = "T0000_DifferenceSignal"
//String filename_LockinSignal = "T0000_LockinSignal"
//String filename_ReferenceSignal = "T0000_ReferenceSignal"

LoadWave/G/D/O/A // Load a General Text file, double precision, overwrite
filename= S_filename

//Put the names of the waves into string variables

w0 = GetStrFromList(S_waveNames, 0,";") // time
w1 = GetStrFromList(S_waveNames, 1,";") // channel 1
w2 = GetStrFromList(S_waveNames, 2,";") // channel 2
w3 = GetStrFromList(S_waveNames, 3,";") // channel 3
w4 = GetStrFromList(S_waveNames, 4,";") // channel 4


// Put the data file index (numbers) into the name of each wave for the characters 1-4 (character 0 is "T")
filename_ScopeTime[1,4] = filename[1,4]
filename_Frequency[1,4] = filename[1,4]
filename_Ramp[1,4] = filename[1,4]
filename_FabryPerot[1,4] = filename[1,4]
filename_ProbeSignal[1,4] = filename[1,4]
filename_DifferenceSignal[1,4] = filename[1,4]
//filename_LockinSignal[1,4] = filename[1,4]
//filename_ReferenceSignal[1,4] = filename[1,4]

//Create waves with meaningful names
	Duplicate/O $w0, $filename_ScopeTime
	Wave ScopeTime = $filename_ScopeTime

	Duplicate/O $w0, $filename_Frequency; KillWaves $w0
	Wave Frequency = $filename_Frequency

	Duplicate/O $w1, $filename_Ramp; KillWaves $w1
   Wave/Z Ramp = $filename_Ramp
	
	Duplicate/O $w2, $filename_FabryPerot; KillWaves $w2
	Wave/Z FabryPerot = $filename_FabryPerot

	Duplicate/O $w3, $filename_ProbeSignal; KillWaves $w3
   Wave/Z ProbeSignal = $filename_ProbeSignal

//	Duplicate/O $w3, $filename_ReferenceSignal; KillWaves $w3
//	Wave/Z ReferenceSignal = $filename_ReferenceSignal

	Duplicate/O $w4, $filename_DifferenceSignal; KillWaves $w4
	Wave/Z DifferenceSignal = $filename_DifferenceSignal
	
//	Duplicate/O $w4, $filename_LockinSignal; KillWaves $w4
//	Wave/Z LockinSignal = $filename_LockinSignal
	

// Scale the x data to time:
//	variable dt = (ScopeTime[1] - ScopeTime[0])
	variable dt = (ScopeTime[numpnts(ScopeTime)] - ScopeTime[0])/(numpnts(ScopeTime)-1)
	variable tstart = ScopeTime[0]
	SetScale/P x tstart,dt,"", $Filename_ScopeTime
//	SetScale/P x tstart,dt,"", $Filename_Ramp
	SetScale/P x tstart,dt,"", $Filename_Frequency
	SetScale/P x tstart,dt,"", $Filename_DifferenceSignal
	SetScale/P x tstart,dt,"", $Filename_FabryPerot
	SetScale/P x tstart,dt,"", $Filename_ProbeSignal
//	SetScale/P x tstart,dt,"", $Filename_ReferenceSignal
//	SetScale/P x tstart,dt,"", $Filename_LockinSignal


//Make Graphs

	//GraphTitle0= "Graph_" + filename_DifferenceSignal
	//Display $filename_DifferenceSignal as GraphTitle0
	//SetAxis Bottom -2 , 0
	//ModifyGraph mirror=1,standoff=0
	//ModifyGraph tick=2
	
	
	GraphTitle1= "Graph_" + filename_DifferenceSignal
	Display/N=$GraphTitle1 $filename_DifferenceSignal vs $filename_Frequency //as  GraphTitle1
//	SetAxis Bottom -2 , 0
	ModifyGraph mirror=1,standoff=0
	ModifyGraph tick=2
	ShowInfo
	

	GraphTitle2= "Graph_" + filename_FabryPerot
	Display/N=$GraphTitle2 $filename_FabryPerot vs $filename_ScopeTime //as GraphTitle2
	//SetAxis Bottom -2 , 0
	ModifyGraph mirror=1,standoff=0
	ModifyGraph tick=2

End

Function LoadSingleScopeData()

// When outputing a single trace the scope outputs two columns per trace: value and "Peak Detect"
// This function assumes that all four traces are saved


String pathName
String filename
String w0, w1, w2, w3, w4, w5, w6, w7, w8
String GraphName0, GraphName1,GraphName2,GraphName3
String  GraphTitle0,GraphTitle1,GraphTitle2,GraphTitle3

String filename_ScopeTime = "T0000_ScopeTime"
String filename_Frequency = "T0000_Frequency"
String filename_Ramp = "T0000_Ramp"
String filename_FabryPerot = "T0000_FabryPerot"
String filename_ProbeSignal = "T0000_ProbeSignal"
//String filename_ReferenceSignal = "T0000_ReferenceSignal"
String filename_DifferenceSignal = "T0000_DifferenceSignal"
//String filename_LockinSignal = "T0000_LockinSignal"

LoadWave/G/D/O/A // Load a General Text file, double precision, overwrite
filename= S_filename

//Put the names of the waves into string variables

w0 = GetStrFromList(S_waveNames, 0,";") // time
w1 = GetStrFromList(S_waveNames, 1,";") // channel 1
w2 = GetStrFromList(S_waveNames, 2,";") // channel 2
w3 = GetStrFromList(S_waveNames, 3,";") // channel 3
w4 = GetStrFromList(S_waveNames, 4,";") // channel 4
w5 = GetStrFromList(S_waveNames, 5,";") // channel 3
w6 = GetStrFromList(S_waveNames, 6,";") // channel 4
w7 = GetStrFromList(S_waveNames, 7,";") // channel 3
w8 = GetStrFromList(S_waveNames, 8,";") // channel 4


// Put the data file index (numbers) into the name of each wave for the 4th, 5th, and 6th characters
filename_ScopeTime[1,4] = filename[1,4]
filename_Frequency[1,4] = filename[1,4]
filename_Ramp[1,4] = filename[1,4]
filename_DifferenceSignal[1,4] = filename[1,4]
//filename_LockinSignal[1,4] = filename[1,4]
filename_FabryPerot[1,4] = filename[1,4]
filename_ProbeSignal[1,4] = filename[1,4]
//filename_ReferenceSignal[1,4] = filename[1,4]

//Create waves with meaningful names
	Duplicate/O $w0, $filename_ScopeTime
	Wave ScopeTime = $filename_ScopeTime

	Duplicate/O $w0, $filename_Frequency; KillWaves $w0
	Wave Frequency = $filename_Frequency

	Duplicate/O $w1, $filename_Ramp; KillWaves $w1, $w2
   Wave/Z Ramp = $filename_Ramp
	
	Duplicate/O $w3, $filename_FabryPerot; KillWaves $w3, $w4
	Wave/Z FabryPerot = $filename_FabryPerot

	Duplicate/O $w5, $filename_ProbeSignal; KillWaves $w5,$w6
	Wave/Z ProbeSignal = $filename_ProbeSignal

//	Duplicate/O $w3, $filename_ReferenceSignal; KillWaves $w3
//	Wave/Z ReferenceSignal = $filename_ReferenceSignal

	Duplicate/O $w7, $filename_DifferenceSignal; KillWaves $w7,$w8
	Wave/Z DifferenceSignal = $filename_DifferenceSignal
	
//	Duplicate/O $w7, $filename_LockinSignal; KillWaves $w7,$w8
//	Wave/Z LockinSignal = $filename_LockinSignal
	



// Scale the x data to time:
//	variable dt = (ScopeTime[1] - ScopeTime[0])
	variable dt = (ScopeTime[numpnts(ScopeTime)] - ScopeTime[0])/(numpnts(ScopeTime)-1)
	variable tstart = ScopeTime[0]
	SetScale/P x tstart,dt,"", $Filename_ScopeTime
	SetScale/P x tstart,dt,"", $Filename_Ramp
	SetScale/P x tstart,dt,"", $Filename_Frequency
	SetScale/P x tstart,dt,"", $Filename_DifferenceSignal
	SetScale/P x tstart,dt,"", $Filename_FabryPerot
//	SetScale/P x tstart,dt,"", $Filename_ProbeSignal
//	SetScale/P x tstart,dt,"", $Filename_ReferenceSignal
//	SetScale/P x tstart,dt,"", $Filename_LockinSignal


//Make Graphs

	//GraphTitle0= "Graph_" + filename_DifferenceSignal
	//Display $filename_DifferenceSignal as GraphTitle0
	//SetAxis Bottom -2 , 0
	//ModifyGraph mirror=1,standoff=0
	//ModifyGraph tick=2
	
	
	GraphTitle1= "Graph_" + filename_DifferenceSignal
	Display/N=$GraphTitle1 $filename_DifferenceSignal vs $filename_Frequency //as  GraphTitle1
//	SetAxis Bottom -2 , 0
	ModifyGraph mirror=1,standoff=0
	ModifyGraph tick=2
	ShowInfo
	

	GraphTitle2= "Graph_" + filename_FabryPerot
	Display/N=$GraphTitle2 $filename_FabryPerot vs $filename_ScopeTime //as GraphTitle2
	//SetAxis Bottom -2 , 0
	ModifyGraph mirror=1,standoff=0
	ModifyGraph tick=2

End


// This routine will look at the Fabry-Perot scan, find the peaks, and re-scale the spectrum to frequency.

Function  FabryPerotCalibration()
	
	Variable NumPeaks = 28
	Variable PeakThreshold = 0.3
	Variable FSR = 91.5
	Variable StartTime = 0.0025
	Variable StartIndex = 0
	String GraphTitle,TableTitle

	String FabryWaveName
	Prompt NumPeaks, " Number of Peaks: "
	Prompt StartTime, " Time to Start Looking for Peaks: "
	Prompt StartIndex, " Peak # for first peak: "
	Prompt FabryWaveName, " Fabry Perot Wave: ", popup, WaveList("*_FabryPerot", ";", "")
	Prompt PeakThreshold, " Peak Threshold Value: "
	Prompt FSR, " Free Spectral Range: "


	DoPrompt "Calibrate FP",FabryWaveName, StartTime, StartIndex NumPeaks, PeakThreshold,FSR

	String FrequencyWaveName = "T0000_Frequency"
	FrequencyWaveName[1,4] = FabryWaveName[1,4]
	print FrequencyWaveName
	
	String PeakLocationWaveName = "T0000_PeakLocation"
	PeakLocationWaveName[1,4] = FabryWaveName[1,4]
	String PeakFrequencyWaveName = "T0000_PeakFrequency"
	PeakFrequencyWaveName[1,4] = FabryWaveName[1,4]
	print PeakLocationWaveName, PeakFrequencyWaveName

	
	Make/N=(NumPeaks)/D/O	$PeakLocationWaveName
	Make/N=(NumPeaks)/D/O	$PeakFrequencyWaveName
 
 	print FabryWaveName, NumPeaks, PeakThreshold
 	
 	WAVE FabryWave = $FabryWaveName
	WAVE FrequencyWave = $FrequencyWaveName
 	WAVE PeakLocation = $PeakLocationWaveName
	WAVE PeakFrequency = $PeakFrequencyWaveName
	
	TableTitle = "Table_" + PeakLocationWaveName
	DoWindow/F $TableTitle
	if (V_flag == 0) //Window doesn't exist
		Print "Table V_flag = ", V_flag 
	   Edit/N=$TableTitle PeakFrequency,PeakLocation //as TableTitle
	Endif
	Variable LastPeak = leftx(FabryWave)
	LastPeak = StartTime
	Print "LastPeak[0] = ", LastPeak

	Variable i
	for(i=0; i<NumPeaks; i+=1)
		FindPeak/Q/M=(PeakThreshold)/B=1/R=(LastPeak+20*deltax(FabryWave),inf) FabryWave 	//Finds the ith peak on the fabry perot scope (location outputs reported as x-values)
//		FindPeak/Q/M=(PeakThreshold)/B=1 FabryWave 	//Finds the ith peak on the fabry perot scope (location outputs reported as x-values)
		PeakLocation[i]=V_PeakLoc		 //x-location of ith peak on FP scope
		LastPeak = V_PeakLoc
		PeakFrequency[i] = (i + StartIndex)*FSR
//		print "LastPeak = ", LastPeak
	endfor

	GraphTitle= "Graph_" + PeakFrequencyWaveName
	DoWindow/F $GraphTitle
	if (V_flag == 0) //Window doesn't exist
		Display/N=$GraphTitle PeakFrequency vs PeakLocation // as GraphTitle
	Endif

	CurveFit/Q poly 6, PeakFrequency /X=PeakLocation /D /R
	Wave W_coef
	print "a = ", W_coef[0], "b = ", W_coef[1],"c = ", W_coef[2],"d = ", W_coef[3], "e = ", W_coef[4], "f = ", W_coef[5]
	
	FrequencyWave = W_coef[0] + W_coef[1]*x + W_coef[2]*x^2 +  W_coef[3]*x^3 +  W_coef[4]*x^4 +  W_coef[5]*x^5 
	
End




// This routine will look at the Fabry-Perot scan, find the peaks, and re-scale the spectrum to frequency.

Function  FabryPerotCalibration_Smooth()
	
	Variable NumPeaks = 23
	Variable PeakThreshold = 1.5
	Variable FSR = 91.5
	Variable StartTime = -2
	Variable StartIndex = 0
	Variable BoxSize = 21
	String GraphTitle,TableTitle

	String FabryWaveName
	Prompt NumPeaks, " Number of Peaks: "
	Prompt StartTime, " Time to Start Looking for Peaks: "
	Prompt StartIndex, " Peak # for first peak: "
	Prompt FabryWaveName, " Fabry Perot Wave: ", popup, WaveList("*_FabryPerot", ";", "")
	Prompt PeakThreshold, " Peak Threshold Value: "
	Prompt BoxSize, " Box Smoothing Parameter: "
	Prompt FSR, " Free Spectral Range: "


	DoPrompt "Calibrate FP",FabryWaveName, StartTime, StartIndex NumPeaks, PeakThreshold,BoxSize,FSR

	String FrequencyWaveName = "T0000_Frequency"
	FrequencyWaveName[1,4] = FabryWaveName[1,4]
	print FrequencyWaveName
	
	String PeakLocationWaveName = "T0000_PeakLocation"
	PeakLocationWaveName[1,4] = FabryWaveName[1,4]
	String PeakFrequencyWaveName = "T0000_PeakFrequency"
	PeakFrequencyWaveName[1,4] = FabryWaveName[1,4]
	print PeakLocationWaveName, PeakFrequencyWaveName

	
	Make/N=(NumPeaks)/D/O	$PeakLocationWaveName
	Make/N=(NumPeaks)/D/O	$PeakFrequencyWaveName
 
 	print FabryWaveName, NumPeaks, PeakThreshold
 	
 	WAVE FabryWave = $FabryWaveName
	WAVE FrequencyWave = $FrequencyWaveName
 	WAVE PeakLocation = $PeakLocationWaveName
	WAVE PeakFrequency = $PeakFrequencyWaveName
	
	TableTitle = "Table_" + PeakLocationWaveName
	DoWindow/F $TableTitle
	if (V_flag == 0) //Window doesn't exist
		Print "Table V_flag = ", V_flag 
	   Edit/N=$TableTitle PeakFrequency,PeakLocation //as TableTitle
	Endif
	Variable LastPeak = leftx(FabryWave)
	LastPeak = StartTime
	Print "LastPeak[0] = ", LastPeak

	Variable i
	for(i=0; i<NumPeaks; i+=1)
		FindPeak/Q/M=(PeakThreshold)/B=(BoxSize)/R=(LastPeak+20*deltax(FabryWave),inf) FabryWave 	//Finds the ith peak on the fabry perot scope (location outputs reported as x-values)
//		FindPeak/Q/M=(PeakThreshold)/B=1 FabryWave 	//Finds the ith peak on the fabry perot scope (location outputs reported as x-values)
		PeakLocation[i]=V_PeakLoc		 //x-location of ith peak on FP scope
		LastPeak = V_PeakLoc
		PeakFrequency[i] = (i + StartIndex)*FSR
//		print "LastPeak = ", LastPeak
	endfor

	GraphTitle= "Graph_" + PeakFrequencyWaveName
	DoWindow/F $GraphTitle
	if (V_flag == 0) //Window doesn't exist
		Display/N=$GraphTitle PeakFrequency vs PeakLocation // as GraphTitle
	Endif

	CurveFit/Q poly 5, PeakFrequency /X=PeakLocation /D /R
	Wave W_coef
	print "a = ", W_coef[0], "b = ", W_coef[1],"c = ", W_coef[2],"d = ", W_coef[3], "e = ", W_coef[4], "f = ", W_coef[5]
	
	FrequencyWave = W_coef[0] + W_coef[1]*x + W_coef[2]*x^2 +  W_coef[3]*x^3  +  W_coef[4]*x^4 //+  W_coef[5]*x^5 
	
End
