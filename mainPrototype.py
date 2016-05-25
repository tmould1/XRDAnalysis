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

    global equationType
    equationType = -1
    
    # get theoretical filename
    askStructureType = str(raw_input("Enter the number corresponding to your sample structure: 0-cubic, 1-tetragonal, 2-orthorhombic, 3-hexagonal :  "))
    equationType = float(askStructureType)
    print equationType
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
    print equationType
    # determine equation type
    if equationType == 0:
        # Create an Object from Class Instantiation
        solver = xrdClasses.CubicEquation()
    elif equationType == 1:
        solver = xrdClasses.TetragonalEquation()
    elif equationType == 2:
        solver = xrdClasses.OrthorhombicEquation()
    elif equationType == 3:
        solver = xrdClasses.HexagonalEquation()
    i = 2
    j = 0
    hkl = []
    h = 0
    k = 0
    l = 0
    global a,b,c
    a = []
    b = []
    c = []
    aPoint = 0
    bPoint = 0
    cPoint = 0
    for point in theoreticalSet:
        hkl = point.getIdentifier().Report()
        inD = point.data.invDSqr
        h = hkl[0]
        k = hkl[1]
        l = hkl[2]
        print hkl
        if equationType == 0:
            aPoint = solver.solve(point)
            a.append(a)
            print a
        elif equationType == 1:
            if i%2==0:
                point1 = point
            else:
                [aPoint,cPoint] = solver.solve(point1,point)
                a.append(a)
                c.apppend(c)
        elif equationType == 2:
##            if h == 0 and k == 0:
##               c = l/inD
##            elif h == 0 and l == 0:
##                b = k/inD
##            elif k == 0 and l == 0:
##                a = h/inD
##            
##            elif i
            if j == 0:
                point1 = point
                j+=1
            elif j == 1:
                point2 = point
                j+=1
            elif j == 2:
                [a,b,c] = solver.solve(point1,point2,point)
                j = 0
                
        elif equationType == 3:
            if i%2==0:
                point1 = point
            else:
                print solver.solve(point1,point)
        i+=1
            
    
        
        
        
        
    
        
        
##        thetaRad = math.radians(point.twoTheta)
##        if equationType == 0:
##            print solver.solve(point)
##            break
##       
##        AddDataPoint( thetaRad, processedTheoreticalSet )
                      
    

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
experimentalSet = []
processedTheoreticalSet = []
processedExperimentalSet = []
##equationType = -1
a = []
b = []
c = []
main()





    
