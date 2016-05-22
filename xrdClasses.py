import math
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
        return self.get()


class TheoreticalDataPoint:
    intensity = 0
    percentI = 0
    indices = MillerIndices(0,0,0)
    dVal = 0
    twoTheta = 0
    id = -1
    invDSqr = 0


    def set(self, inInt, inPercInt, inD, inTwoTheta, inId):
        self.intensity = inInt
        self.percentI = inPercInt
        self.dVal = inD
        self.twoTheta = inTwoTheta
        self.id = inId
        self.invDSqr = pow(self.dVal,-2)
        

    def __init__(self, inInt, inPerc, inD, inTwoTheta, inId):
        self.set( inInt, inPerc, inD, inTwoTheta, inId )

    def get(self):
        data =  [self.id, self.intensity, self.percentI, self.invDSqr, self.twoTheta]
        return data

    def setIdentifier(self, ih, ik, il):
        self.indices = MillerIndices(ih,ik,il)

    def getIdentifier(self):
        return self.indices

    def Report(self):
        return self.get()

class ExperimentalDataPoint:
    indices = MillerIndices(0,0,0)
    intensity = 0
    twoTheta = 0
    dVal = 0
    ratios = []
    id = -1


    def __init__(self, inInt, inTwoTheta, inId):
        self.set( inInt, inTwoTheta, inId )
        
    def set(self, inInt, inTwoTheta, inId):
        self.intensity = inInt
        self.twoTheta = inTwoTheta
        self.id = inId

    def get(self):
        data =  [self.twoTheta, self.intensity, self.id]
        return data

    def calcDValue(self):
        return 1

    def calcRatios(self, dataSet):
        return 1

    def getIdentifier(self):
        return self.indices.get()


class CubicEquation:
    a = 0

    def solve(self, point):
        h = point.indices.h
        k = point.indices.k
        l = point.indices.l
        result = math.sqrt((pow(h,2)+pow(k,2)+pow(l,2))/point.invDSqr)
        self.a = result
        return result

class TetragonalEquation:
    a = 0
    c = 0

    def solve(self, point1, point2):
        h1 = point1.indices.h
        h2 = point2.indices.h
        k1 = point1.indices.k
        k2 = point2.indices.k
        l1 = point1.indices.l
        l2 = point2.indices.l
        inD1 = point1.invDSqr
        inD2 = point2.invDSqr
        self.c = math.sqrt(((pow(h2,2)+pow(k2,2))*(pow(l1,2)/(pow(h1,2)+pow(k1,2))))/(inD2+inD1*(pow(h2,2)+pow(k2,2))/(pow(h1,2)+pow(k1,2))))
        self.a = math.sqrt((pow(h1,2)+pow(k1,2))/((pow(l1,2)/pow(self.c,2))-inD1))
        return [self.a, self.c]

class OrthogonalEquation:
    a = 0
    b = 0
    c = 0

    def solve(self, point1, point2, point3):
        h1 = point1.indices.h
        h2 = point2.indices.h
        h3 = point3.indices.h
        k1 = point1.indices.k
        k2 = point2.indices.k
        k3 = point3.indices.k
        l1 = point1.indices.l
        l2 = point2.indices.l
        l3 = point3.indices.l
        inD1 = point1.invDSqr
        inD2 = point2.invDSqr
        inD3 = point3.invDSqr
        self.c = math.sqrt((inD3 - inD1*pow(h3,2)/pow(h1,2) - ((pow(k3,2)-pow(k1,2)*pow(h3,2)/pow(h1,2))*(inD2-inD1*pow(h2,2)/pow(h1,2))/(pow(k2,2)-pow(k1,2)*pow(h2,2)/pow(h1,2))))/(pow(l3,2)-pow(l1,2)*pow(h3,2)/pow(h1,2)-(pow(l2,2)-pow(l1,2)*pow(h2,2)/pow(h1,2))*((pow(k3,2)-pow(k1,2)*pow(h3,2)/pow(h1,2))/(pow(k2,2)-pow(k1,2)*pow(h3,2)/pow(h1,2)))))
        self.b = 
        return [self.a, self.c]


