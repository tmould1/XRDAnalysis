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
import csv

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

    # get theoretical filename
    thFileName = str(raw_input("Enter Theoretical File Name:"))
    while status == 0:
    
        # open file
        status = fileCheck( thFileName )

        # no good?
        if status == 0:
            thFileName = str(raw_input('Please enter the correct File Name: '))
            
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
    with open( xpFileName ) as csvfile:
        f = csv.reader(csvfile, delimiter=' ')

        for line in f:
            # Strip the line into words
            
            twoTheta = float(line[0])
            intensity = float(line[1])
        
            # Make Data Point object
            iDataPoint = xrdClasses.ExperimentalDataPoint( intensity, twoTheta, i )
            
            # Add Data point to list
            AddDataPoint( iDataPoint, experimentalSet )
            i+=1
        
            # END FOR
    
    csvfile.close()   

    if status:
        print 'Got experimental data'
    else:
        print 'Did not get experimental data'


# Process Data
def processData():
    # determine equation type
    # Assuming Cubic for Show

    # Create an Object from Class Instantiation
    cSolver = xrdClasses.CubicEquation()
    
    for point in theoreticalSet:
        thetaRad = math.radians(point.twoTheta)
        print cSolver.solve(point)
        AddDataPoint( thetaRad, processedTheoreticalSet )\
                      
    

# calculate d-ratios
def calcRatios():
    print 'calculated d-ratios'

# Check Info for epsilon neighborhood
def checkInfo():
    print 'checked for points within specified range'

# Calculate Lattice Constants
def calcLattice():
    print 'Calculated the lattice constants'

# Report necessary information in appropriate location
def report():
##    for datapoint in theoreticalSet:
##        print "MillerIndices: ", datapoint.indices.Report()
##        print "Data: ", datapoint.Report()
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
    #getExperimentalData()

    processData()

    calcRatios()
    checkInfo()
    calcLattice()

    # Proof of Concepts
    #AddPointPOC()
    # End Proof of Concepts

    report()

# Procedure
theoreticalSet = []
experimentalSet = []
processedTheoreticalSet = []
processedExperimentalSet = []
main()





    
