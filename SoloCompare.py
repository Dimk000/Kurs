import numpy as np

def solocomp(M, M1):
    structCount = 0
    counter1 = 0
    structValue1 = np.zeros(3600)
    structValue2 = np.zeros(3600)
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j] != 0 and M1[i][j] != 0:
                structCount += 1
                structValue1[counter1] = M[i][j]
                structValue2[counter1] = M1[i][j]
                counter1 += 1
    overall1 = len(np.transpose(np.nonzero(M)))
    overall2 = len(np.transpose(np.nonzero(M1)))
    structDif = abs(structValue2-structValue1)
    structDif_sum = sum(structDif)
    diffCount = len(np.transpose(np.nonzero(np.array(M != M1))))
    # return overall1, overall2, structDif, structDif_sum, diffCount
    print('Сравнение двух структур')
    print('Общее колличесво элементов в первой структуре: ', overall1)
    print('Во второй структуре: ', overall2)
    print('Колличество совпадений в струкутрах равно ', structCount)
    print('Колличество несовпадений в струкутрах равно ', diffCount)
    print('Разница значений в точках совпадения составляет ', structDif)
    print('Суммарная разность значений состовляет ', structDif_sum)
