# XRD Analysis
# Emily Kramer and Todd Moulder
# 5/17/16
# For Research Purposes
#  To Compare theoretical data with experimental data
#    in order to identify peak matching for candidate subtances
#
# input:  theoretical and experimental xrd data files, structure
# output: theoretical and experimental lattice constants, volume, and plots

import xrdClasses
import math
import numpy as np
import scipy as sp
from scipy import signal
import matplotlib as mpl
import matplotlib.pyplot as plt

#############
#  List Helper Functions
#############

#add an element to the end of a set
def AddDataPoint( point, dataSet ):
    dataSet.append(point)

#get an element from a set, removing it from the set in the process
def GetDataPoint( position, dataSet ):
    data = dataSet.pop(position)
    return data

#place an element at a specific location in the set; useful if you've used GetDataPoint
def PlaceDataPoint( point, position, dataSet):
    dataSet.insert(position, point)


#############
#  Main Helper Functions
#############

### file check
##def fileCheck( FileName ):
##    try:
##        File = open( FileName )
##    except IOError:
##        print 'Cannot open "', FileName, '"'
##        File = str(raw_input('Please enter the correct File Name: '))
##    else:
##        print FileName, ' opened successfully'

def fileCheck( fileName ) :
    status = 1
    try:
        f = open(fileName)
    except IOError:
        status = 0
    finally:
        if status == 1:
            f.close()

    return status

#get theoretical data
def getTheoreticalData():
    status = 0

    global equationType
    equationType = -1
    
    # get theoretical filename
    askStructureType = str(raw_input("Enter the number corresponding to your sample structure: 0-cubic, 1-tetragonal, 2-orthorhombic, 3-hexagonal :  "))
    equationType = int(askStructureType)
    thFileName = str(raw_input("Enter Theoretical File Name:  "))
    while status == 0:
    
        # open file
        status = fileCheck( thFileName )

        # no good?
        if status == 0:
            thFileName = str(raw_input('Please enter the correct File Name:  '))
            
    # Initialize data point counter
    i = 0
    
    # open file for reading
    f = open( thFileName )
    j = 0
    for line in f:
        if j < 9:
            j+=1
            continue

        # Strip the line into words
            
        line = line.strip()
        line = line.split()

        # End of File Condition
        if '*' in line[0]:
            break

        # Acquire Data
        h = int(line[0])
        k = int(line[1])
        l = int(line[2])
        d = float(line[3])
        twoTheta = float(line[4])
        intensityString = line[5]
        intensityTriple = intensityString.partition('e')
        intensity = pow(float(intensityTriple[0]),float(intensityTriple[2]))
        percentImax = float(line[6].rstrip('%'))
   
        # Make Data Point object and load info
        iDataPoint = xrdClasses.TheoreticalDataPoint( intensity, percentImax, d, twoTheta, i )
        iDataPoint.setIdentifier(h,k,l)
            
        # Add Data point to list
        AddDataPoint( iDataPoint, theoreticalSet )
        i+=1
        
    # END FOR
    
    f.close()  

    if status:
        print 'Got theoretical data'
    else :
        print 'Did not get theoretical data'

#get experimental data
def getExperimentalData():
    status = 0

    # get experimental filename
    xpFileName = str(raw_input("Enter Experimental File Name:"))

    
    while status == 0:    
        # open file
        status = fileCheck( xpFileName )

        # no good?
        if status == 0:
            xpFileName = str(raw_input('Please enter the correct File Name: '))
            
    # Initialize data point counter
    i = 0
    
    # open file for reading
    f = open( xpFileName )

    # Initialize Imax variable
    Imax = 0
    intensityArray = []
    for line in f:
        i+=1
        if i<=367:
            continue
        else:
            # Strip the line into words
            line = line.strip()
            line = line.split()
            twoTheta = float(line[0])
            intensity = float(line[1])
            if intensity>Imax:
                Imax = intensity
           
            # Make Data Point object
            iDataPoint = xrdClasses.ExperimentalDataPoint( intensity, twoTheta, i )
            
            # Add Data point to list
            AddDataPoint( iDataPoint, experimentalSet )
            AddDataPoint( intensity, instensityArray )
            i+=1
    
        # END FOR
    
    f.close()

    peaks = signal.find_peaks_cwt( intensityArray, 0.07, gap_thresh=30 )
    print peaks
    

##    points = []
##    i = 0
##    for point in experimentalSet:
##        if len(points)<=20:
##            AddDataPoint( point, points )
##            continue
##        points = sorted(points, key=lambda point:point.intensity, reverse=True)
##        if point.Report()[1]>points[i].Report()[1]:
##            if abs(point.Report()[0]-points[i].Report()[0])<0.01:
##                GetDataPoint( i, points )
##                PlaceDataPoint( point, i, points )
##            else:
##                AddDataPoint( point, points )
##                i+=1
##        else:
##            continue
##    print len(points)
##    
##    print len(points)
##    for j in range(1, len(points)):
##        if j > 20:
##            GetDataPoint( j-1, points )
##    print len(points)
##
##    global xpDRatios
##    xpDRatios = []
##    inDValues = []
##    for point in points:
##        AddDataPoint( point.Report()[0], inDValues )
##    for i in range(0,len(inDValues)):
##        inDi = inDValues[i]
##        for j in range(i+1, len(inDValues)):
##            inDj = inDValues[j]
##            inDRatio = inDi/inDj
##            AddDataPoint( inDRatio, xpDRatios )
            
        
        
    
    if status:
        print 'Got experimental data'
    else:
        print 'Did not get experimental data'


# Process Data
def processData():
##    print equationType

    # Find Max Intensity Points
    topIntensityPoints = findMaxIntensities()

    points = []
    # determine Equation Solver Class
    if equationType == 0:
        solver = xrdClasses.CubicEquation()
    elif equationType == 1:
        solver = xrdClasses.TetragonalEquation()
    elif equationType == 2:
        solver = xrdClasses.OrthorhombicEquation()
    elif equationType == 3:
        solver = xrdClasses.HexagonalEquation()

    for point in topIntensityPoints:

        AddDataPoint(point, points)
        if equationType == 0:
            if len(points) > 1:
                GetDataPoint( 0, points )
            AddDataPoint( solver.solve(points[0]), latticeConstants )

        elif equationType == 1:
            if len(points) < 2:
                continue
            elif len(points) == 2:
##                GetDataPoint( 0, points )
                AddDataPoint( solver.solve(points[0], points[1]), latticeConstants )
        elif equationType == 2:
            if len(points) < 3:
                continue
            elif len(points) == 3:
                AddDataPoint( solver.solve(points[0], points[1], points[2]), latticeConstants)
        
        elif equationType == 3:
            if len(points) < 2:
                continue
            elif len(points) == 2:
##                GetDataPoint( 0, points )
                AddDataPoint( solver.solve(points[0], points[1]), latticeConstants )

            
       

# calculate d-ratios
def calcRatios():
    inDValues = []
    thDRatios = []
    topIntensityPoints = findMaxIntensities()
    for point in topIntensityPoints:
        AddDataPoint( point.Report()[3], inDValues )
    for i in range( 0,len(inDValues)):
        inDi = inDValues[i]
        for j in range( i+1,len(inDValues)):
            inDj = inDValues[j]
            inDRatio = inDi/inDj
            AddDataPoint( inDRatio, thDRatios )
        
    print 'calculated d-ratios'

# Check Info for epsilon neighborhood
def checkInfo():
    print 'checked for points within specified range'

# Calculate Lattice Constants
def calcLattice():
    print 'Calculated the lattice constants'

# Grab top intensities
def findMaxIntensities():
    points = []
    for point in theoreticalSet:
##        print point.Report()
        hkl = point.getIdentifier().Report()
        result = hkl[0]+hkl[1]+hkl[2]
        if result%2==1:
            continue
        elements = point.Report()
        if len(points)<=10:
            AddDataPoint( point, points )
        if len(points)>10:
            points = sortOnIntensity( points )
            GetDataPoint( 10, points )

##    print 'Finished Grabbing Top Intensities, they follow: '
##    for item in points:
##        print item.Report()[2]
    return points

# Sort by Intensity
def sortOnIntensity( intArray ):
    return sorted(intArray, key=lambda point: point.percentI, reverse=True)
    

# Report necessary information in appropriate location
def report():
##    for datapoint in theoreticalSet:
##        print "MillerIndices: ", datapoint.indices.Report()
##        print "Data: ", datapoint.Report()
##    for point in latticeConstants:
##        print point
    print 'All data reported to specified location'

###############
# Proof Of Concept Section
###############

def AddPointPOC():
    print "Proof of Concept:  Adding and Retrieving from List"

    # Adding a Theoretical and Experimental Data Point to the set of all respective points
    testTheoreticalPoint = xrdClasses.TheoreticalDataPoint( 0.5, 1, 0 )
    testTheoreticalPoint.setIdentifier( 1, 0, 0 )
    AddDataPoint( testTheoreticalPoint, theoreticalSet )

    testTheoreticalPoint = xrdClasses.TheoreticalDataPoint( 0.75, 1, 1 )
    testTheoreticalPoint.setIdentifier( 0, 1, 0 )
    AddDataPoint( testTheoreticalPoint, theoreticalSet )

    # ExperimentalDataPoint Constructor to be more defined later, should increase number of input paramters
    testExperimentalPoint = xrdClasses.ExperimentalDataPoint( 0.5,1,0 )
    testExperimentalPoint.indices.set( 0, 1, 0 )
    AddDataPoint( testExperimentalPoint, experimentalSet )

###############
# END Proof Of Concept Section
###############
    
# main
def main():

    
    
    getTheoreticalData()
    getExperimentalData()

    processData()
    print "processed data"

    calcRatios()
    checkInfo()
    calcLattice()

    # Proof of Concepts
    #AddPointPOC()
    # End Proof of Concepts

    report()

# Procedure
theoreticalSet = []
theoreticalSetRefined = []
experimentalSet = []
experimentalSetRefined = []
processedTheoreticalSet = []
processedExperimentalSet = []
latticeConstants = []
##equationType = -1
a = []
b = []
c = []
main()





    
