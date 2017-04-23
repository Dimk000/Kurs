import numpy as np

def FreqToStruct(self, wStep, quantStep, MassForRes, S, WFCoeff):
    StepInArray = int(wStep / (MassForRes[1] - MassForRes[0]))
    wPoints = np.zeros(100)
    count = 0
    l = 0
    while count < len(MassForRes):
        wPoints[l] = (MassForRes[count])
        count += StepInArray
        l += 1
    # print(wPoints)   работает!
    count = 0
    l = 0
    sPoints = np.zeros(100)
    while count < len(S):
        sPoints[l] = S[count]
        count += StepInArray
        l += 1
    # квантование
    SPointsQuint = np.zeros(100)
    for i in range(len(sPoints)):
        SPointsQuint[i] = abs(round(sPoints[i], quantStep))
        print(SPointsQuint[i])
    # Quant = abs(quant(SPoints, quantStep))
    # print(SPoints)
    M = np.zeros(len(SPointsQuint)) * len(SPointsQuint)
    self.axes.plot(wPoints, abs(SPointsQuint), 'go', linestyle='steps--')
    self.canvas.draw()