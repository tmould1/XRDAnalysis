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

class OrthorhombicEquation:
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
        h21Sqr = pow(h2/h1,2)
        h31Sqr = pow(h3/h1,2)
        cNum = pow(l3,2)-pow(l1,2)*h31Sqr-(pow(l2,2)-pow(l1,2)*h21Sqr)*(pow(k3,2)-pow(k1,2)*h31Sqr)/(pow(k2,2)-pow(k1,2)*h21Sqr)
        cDen = inD3-inD1*h31Sqr-(inD2-inD1*h21Sqr)*(pow(k3,2)-pow(k1,2)*h31Sqr)/(pow(k2,2)-pow(k1,2)*h21Sqr)
        self.c = math.sqrt(cNum/cDen)
        bNum = pow(k2,2)-pow(k1,2)*h21Sqr
        bDen = inD2-inD1*h21Sqr-(pow(l2,2)-pow(l1,2)*h21Sqr)/pow(self.c,2)
        self.b = math.sqrt(bNum/bDen)
        self.a = h1/math.sqrt(inD1-pow(k1,2)/pow(self.b,2)-pow(l1,2)/pow(self.c,2))
        return [self.a, self.b, self.c]

class HexagonalEquation:
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
        l21Sqr = pow(l2/l1,2)
        self.a = 2*math.sqrt((pow(h2,2)+h2*k2+pow(k2,2)-l21Sqr*(pow(h1,2)+h1*k1+pow(k1,2)))/(3*(inD2-inD1*l21Sqr)))
        self.c = l1/math.sqrt(inD1-4*(pow(h1,2)+h1*k1+pow(k1,2))/(3*pow(self.a,2)))
        return [self.a, self.c]
