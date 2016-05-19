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
        f.close()

    return status
        


#get theoretical data
def getTheoreticalData():
    status = 0
    while status == 0:
        # get theoretical filename
        thFileName = str(raw_input("Enter Theoretical File Name:"))
    
        # open file
        status = fileCheck( thFileName )

        # no good?
        if status == 0:
            thFileName = str(raw_input('Please enter the correct File Name: '))
        
     
    # put Intensity, h,k,l & d-vals into an object
    # open file for reading
    f = open( thFileName )
    # initialize lists
    th_I = []
    th_d = []
    th_h = []
    th_k = []
    th_l = []
    for line in f:
        line = line.strip()
        columns = line.split()
        AddDataPoint( columns[0], th_I )
        AddDataPoint( columns[1], th_d )
        AddDataPoint( columns[2], th_h )
        AddDataPoint( columns[3], th_k )
        AddDataPoint( columns[4], th_l )
    f.close()
    # Use AddDataPoint( data, theoreticalSet);  - Todd

    if status:
        print 'Got theoretical data'
    else :
        print 'Did not get theoretical data'

#get experimental data
def getExperimentalData():
    status = 0
    while status == 0:
        # get experimental filename
        xpFileName = str(raw_input("Enter Experimental File Name:"))
    
        # open file
        status = fileCheck( xpFileName )

        # no good?
        if status == 0:
            xpFileName = str(raw_input('Please enter the correct File Name: '))
        
    
    # put Intensity & 2theta-vals into an object
    # open file for reading
    f = open( xpFileName )
    # initialize lists
    xp_2theta = []
    xp_I = []
    
    f.close()
    # Use AddDataPoint( data, experimentalSet );  - Todd
    if status:
        print 'Got experimental data'
    else:
        print 'Did not get experimental data'

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

    print 'All data reported to specified location'
    
# main
def main():  
    getTheoreticalData()
    getExperimentalData()

    calcRatios()
    checkInfo()
    calcLattice()
    
    report()

    # Proof of Concept
    print "Proof of Concept:  Adding and Retrieving from List"

    # Adding a Theoretical and Experimental Data Point to the set of all respective points
    testTheoreticalPoint = xrdClasses.TheoreticalDataPoint( 0.5, 1, 0 )
    testTheoreticalPoint.indices.set( 1, 0, 0 )
    #theoreticalSet.append( testTheoreticalPoint )
    AddDataPoint( testTheoreticalPoint, theoreticalSet )

    # ExperimentalDataPoint Constructor to be more defined later, should increase number of input paramters
    testExperimentalPoint = xrdClasses.ExperimentalDataPoint()
    testExperimentalPoint.indices.set( 0, 1, 0 )
    #experimentalSet.append( testExperimentalPoint )
    AddDataPoint( testExperimentalPoint, experimentalSet )

    print GetDataPoint(0, theoreticalSet).getIdentifier()
    print GetDataPoint(0, experimentalSet).getIdentifier()
    # End Proof of Concept

# Procedure
theoreticalSet = []
experimentalSet = []
main()





    
