import numpy as np
import SoloCompare as SC

def FreqToStruct(MassForRes, MassForRes1, S, S1, WFCoeff, WFCoeff1):
    wStep = 0.05
    quantStep = 2
    StepInArray = int(wStep / (MassForRes[1] - MassForRes[0]))
    StepInArray1 = int(wStep / (MassForRes1[1] - MassForRes1[0]))
    wPoints = np.zeros(60)
    wPoints1 = np.zeros(60)
    count = 0
    l = 0
    sPoints = np.zeros(60)
    sPoints1 = np.zeros(60)
    print(len(MassForRes))
    while count < len(MassForRes):
        wPoints[l] = MassForRes[count]
        sPoints[l] = S[count] / sum(WFCoeff)
        count += StepInArray
        l += 1
    l = 0
    count = 0
    while count < len(MassForRes1):
        wPoints1[l] = MassForRes1[count]
        sPoints1[l] = S1[count] / sum(WFCoeff1)
        count += StepInArray1
        l += 1

    print(sPoints)
    print(sPoints1)

    SPointsQuint = np.zeros(60)
    SPointsQuint1 = np.zeros(60)
    for i in range(len(sPoints)):
        SPointsQuint[i] = (abs(round(sPoints[i], quantStep)))
    for i in range(len(sPoints1)):
        SPointsQuint1[i] = (abs(round(sPoints1[i], quantStep)))
    M = np.zeros((60, 60))
    M1 = np.zeros((60, 60))
    for i in range(60):
        M[i] = ((np.array(SPointsQuint) == SPointsQuint[i]).astype(int))
        M[i][i] = 0
        M1[i] = ((np.array(SPointsQuint1) == SPointsQuint1[i]).astype(int))
        M1[i][i] = 0

    for i in range(len(SPointsQuint)):
        temp = np.transpose(np.nonzero(M[i]))
        if sum(temp) > 0:
            for j in range(len(temp)):
                if SPointsQuint[temp[j]] == 0:
                    SPointsQuint[temp[j]] = -1
                M[i][temp[j]] = SPointsQuint[temp[j]]
    for i in range(len(SPointsQuint1)):
        temp1 = np.transpose(np.nonzero(M1[i]))
        if sum(temp1) > 0:
            for j in range(len(temp1)):
                if SPointsQuint1[temp1[j]] == 0:
                    SPointsQuint1[temp1[j]] = -1
                M1[i][temp1[j]] = SPointsQuint1[temp1[j]]
    SC.solocomp(M, M1)
