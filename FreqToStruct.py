import numpy as np
import csv
def FreqToStruct(self, MassForRes, S, WFCoeff):
    wStep = 0.05
    quantStep = 2
    StepInArray = int(wStep / (MassForRes[1] - MassForRes[0]))
    wPoints = np.zeros(60)
    count = 0
    l = 0
    sPoints = np.zeros(60)
    print(len(MassForRes))
    while count < len(MassForRes):
        wPoints[l] = (MassForRes[count])
        sPoints[l] = S[count]
        count += StepInArray
        l += 1
    count = 0
    l = 0

    SPointsQuint = np.zeros(60)
    for i in range(len(sPoints)):
        SPointsQuint[i] = (abs(round(sPoints[i], quantStep)))
    M = np.zeros((60, 60))
    for i in range(60):
        M[i] = ((np.array(SPointsQuint) == SPointsQuint[i]).astype(int))
        M[i][i] = 0

    self.axes.plot(wPoints, abs(SPointsQuint), 'go', linestyle='steps--')
    self.canvas.draw()

    for i in range(len(SPointsQuint)):
        temp = np.transpose(np.nonzero(M[i]))
        if sum(temp) > 0:
            for j in range(len(temp)):
                if SPointsQuint[temp[j]] == 0:
                    SPointsQuint[temp[j]] = -1
                M[i][temp[j]] = SPointsQuint[temp[j]]

    output_file = open("StructNew.csv", "w")
    wrtr = csv.writer(output_file)
    for row in M:
        wrtr.writerow(row)
    output_file.close()

    print(M)
