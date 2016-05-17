class MillerIndices:
    h = 0
    k = 0
    l = 0

    def set(self, inH, inK, inL):
        self.h = inH
        self.k = inK
        self.l = inL

    def __init__(self, inH, inK, inL):
        self.set(inH, inK, inL)

    def get(self):
        indices = [self.h,self.k,self.l]
        return indices

    def Report(self):
        print self.get()


class TheoreticalDataPoint:
    intensity = 0
    indices = MillerIndices(0,0,0)
    dVal = 0
    id = -1

    def set(self, inInt, inDVal, inId):
        self.intensity = inInt
        self.dVal = inDVal
        self.id = inId

    def __init__(self, inInt, inDVal, inId):
        self.set( inInt, inDVal, inId )

    def get(self):
        data = [ self.intensity, self.dVal, self.id ]
        return data

    def getIdentifier(self):
        return self.indices.get()

    def Report(self):
        print self.get()

class ExperimentalDataPoint:
    indices = MillerIndices(0,0,0)
    intensity = 0
    twoTheta = 0
    dVal = 0
    ratios = []
    id = -1

    def set(self):
        return 1

    def get(self):
        return 1

    def calcDValue(self):
        return 1

    def calcRatios(self, dataSet):
        return 1

    def getIdentifier(self):
        return self.indices.get()
        

