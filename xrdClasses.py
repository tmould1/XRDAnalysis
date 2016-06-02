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
    inD = 0
    ratios = []
    id = -1
    wavLen = 1.540562


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
        self.twoTheta = self.twoTheta*math.pi/180
        self.inD = pow(2*math.sin(self.twoTheta)/self.wavLen, 2)
        return [self.inD, self.intensity]

    def calcRatios(self, dataSet):
        return 1

    def getIdentifier(self):
        return self.indices.get()

    def Report(self):
        return self.calcDValue()


class CubicEquation:
    a = 0

    def solve(self, point):
        h = point.indices.h
        k = point.indices.k
        l = point.indices.l
        inD = point.invDSqr
        self.a = math.sqrt((pow(h,2)+pow(k,2)+pow(l,2))/inD)
        return self.a

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
        if l1 == 0:
            self.a = math.sqrt((h1*h1+k1*k1)/inD1)
            try:
                self.c = l2/math.sqrt(inD2-((h2*h2+k2*k2)/(self.a*self.a)))
            except ValueError:
                self.c = 0
         
        elif l2 == 0:
            self.a = math.sqrt((h2*h2+k2*k2)/inD2)
            try:
                self.c = math.sqrt(l1*l1/(inD1-(h1*h1+k1*k1)/(self.a*self.a)))
            except ValueError:
                self.c = 0
        elif h1 == 0 and k1 == 0:
            self.a = 0
            self.c = 0
                
        else:
            alpha = (h2*h2+k2*k2)/(h1*h1+k1*k1)
            cNum = l2*l2-(l1*l1*alpha)
            cDen = inD2-(inD1*alpha)
            try:
                self.c = math.sqrt(cNum/cDen)
            except ValueError:
                self.c = 0
                self.a = 0
            else:
                aNum = (h1*h1+k1*k1)
                try:
                    aDen = inD1-(l1*l1/(self.c*self.c))
                except ZeroDivisionError:
                    self.a = 0
                    self.c = 0
                else:
                    try:
                        self.a = math.sqrt(aNum/aDen)   
                    except (ZeroDivisionError, ValueError):
                        self.a = 0
                        self.c = 0            
            
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
        
##        if h1 == 0 and k1 == 0:
##            self.c = math.sqrt(l1*l1/inD1)
##            h32Sqr = pow(h3/h2,2)
##            l21Sqr = pow(l2/l1,2)
##            bNum = k3*k3-k2*k2*h32Sqr
##            bDen = inD3-h32Sqr*(inD2-l21Sqr*inD1)
##            self.b = math.sqrt(bNum/bDen)
##            self.a = math.sqrt(h2*h2/(inD2-l21Sqr*inD1-pow(k2/self.b,2)))
##        elif h2 == 0 and k2 == 0:
##            self.c = math.sqrt(l2*l2/inD2)
##            h13Sqr = pow(h1/h3,2)
##            l32Sqr = pow(l3/l2,2)
##            bNum = k1*k1-k3*k3*h13Sqr
##            bDen = inD1-h13Sqr*(inD3-l32Sqr*inD2)
##            self.b = math.sqrt(bNum/bDen)
##            self.a = math.sqrt(h3*h3/(inD3-l32Sqr*inD2-pow(k3/self.b,2)))
##        elif h3 == 0 and k3 == 0:
##            self.c = math.sqrt(l3*l3/inD3)
##            h21Sqr = pow(h2/h1,2)
##            l13Sqr = pow(l1/l3,2)
##            bNum = k2*k2-k1*k1*h21Sqr
##            bDen = inD2-h21Sqr*(inD1-l13Sqr*inD3)
##            self.b = math.sqrt(bNum/bDen)
##            self.a = math.sqrt(h1*h1/(inD1-l13Sqr*inD3-pow(k1/self.b,2)))
        if h1 == 0:
            self.a = 0
            self.b = 0
            self.c = 0
        else:
            h21Sqr = pow(h2/h1,2)
            h31Sqr = pow(h3,h1,2)
            cNum = l3*l3-l1*l1*h31Sqr-(l2*l2-l1*l1*h21Sqr)*(k3*k3-k1*k1*h31Sqr)
##            try:
            cDen = inD3-inD1*h31Sqr-(inD2-inD1*h21Sqr)*(k3*k3-k1*k1*h31Sqr)/(k2*k2-k1*k1*h21Sqr)
##            except (ZeroDivisionError, ValueError):
##                self.c = 0
##                self.b = 0
##                self.a = 0
##            else:
##                try:
            self.c = math.sqrt(abs(cNum/cDen))
##                except ValueError:
##                    self.c = 0
##                    self.a = 0
##                    self.b = 0
##                else:
            bNum = k2*k2-k1*k1*h21Sqr
##                    try:
            bDen = inD2-inD1*h21Sqr-(l2*l2-l1*l1*h21Sqr)/(self.c*self.c)
##                    except ZeroDivisionError:
##                        self.a = 0
##                        self.b = 0
##                        self.c = 0
##                    else:
##                        try:
            self.b = math.sqrt(abs(bNum/bDen))
##                        except ValueError:
##                            self.a = 0
##                            self.b = 0
##                            self.c = 0
##                        else:
##                            try:
            self.a = math.sqrt(abs(h1*h1/(inD1-pow(k1/self.b,2)-pow(l1/self.c,2))))
                                
##                            except ValueError:
##                                self.a = 0
##                                self.b = 0
##                                self.c = 0
        print self.a, self.b, self.c
                            
        return [self.a, self.b, self.c]

class HexagonalEquation:
    a = 0
    c = 0
    h = 0
    k = 0
    l = 0
    def solve(self, point1, point2):
        h1 = point1.indices.h
        h2 = point2.indices.h
        k1 = point1.indices.k
        k2 = point2.indices.k
        l1 = point1.indices.l
        l2 = point2.indices.l
        inD1 = point1.invDSqr
        inD2 = point2.invDSqr
       
        if h1>h2 or k1>k2:
            h = h1
            h1 = h2
            k = k1
            k1 = k2
            l = l1
            l1 = l2
        else:
            h = h2
            k = k2
            l = l2
        if l1 == 0:
            self.c = 0
            self.a = 0
        else:
            try:
                l21Sqr = l*l/(l1*l1)
                aNum = 4*(h*h+h*k+k*k-l21Sqr*(h1*h1+h1*k1+k1*k1))
                aDen = 3*(inD2-(inD1*l21Sqr))
                self.a = math.sqrt(aNum/aDen)
                try:
                    self.c = l1/math.sqrt(inD1-(4*(h1*h1+h1*k1*k1*k1)/(3*self.a*self.a)))
                except ValueError:
                    self.c = 0
            except:
                self.c = 0
                self.a = 0
        return [self.a, self.c]
