import xrdClasses

#get theoretical data
def getTheoreticalData():
    status = 1
    # get theoretical filename
    thFileName = str(raw_input("Enter Theoretical Filename:"))
    if not thFileName:
        status = 0
    # error check filename
    # open file
    # error check file open
    # put Intensity, h,k,l & d-vals into an object
    if status:
        print 'Got theoretical data'
    else :
        print 'Did not get theoretical data'

#get experimental data
def getExperimentalData():
    status = 1
    # get experimental filename
    xpFileName = str(raw_input("Enter Experimental Filename:"))
    if not xpFileName:
        status = 0
    # error check filename
    # open file
    # error check file open
    # put Intensity & 2theta-vals into an object
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
    #theorySet = TheoreticalDataPoint[sizeOfDataSet]
    getTheoreticalData()
    getExperimentalData()
    calcRatios()
    checkInfo()
    calcLattice()
    report()

# Procedure
main()





    
