import numpy as np

def FreqToStruct(MassForRes, S, WFCoeff, wStep, quantStep):

    StepInArray = int(wStep / (MassForRes[1] - MassForRes[0]))

    wPoints = np.zeros(60)
    count = 0
    l = 0
    sPoints = np.zeros(60)
    while count < len(MassForRes):
        wPoints[l] = MassForRes[count]
        sPoints[l] = S[count] / sum(WFCoeff)
        count += StepInArray
        l += 1
    SPointsQuint = np.zeros(60)
    for i in range(len(sPoints)):
        SPointsQuint[i] = (abs(round(sPoints[i]/quantStep)*quantStep))
    M = np.zeros((60, 60))
    for i in range(60):
        M[i] = ((np.array(SPointsQuint) == SPointsQuint[i]).astype(int))
        M[i][i] = 0

    for i in range(len(SPointsQuint)):
        temp = np.transpose(np.nonzero(M[i]))
        if sum(temp) > 0:
            for j in range(len(temp)):
                if SPointsQuint[temp[j]] == 0:
                    SPointsQuint[temp[j]] = -1
                M[i][temp[j]] = SPointsQuint[temp[j]]

    return M
