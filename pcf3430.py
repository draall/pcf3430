import re
from pandas import Series, DataFrame

import os

targetFiles = []
listRefKey = []
listRefVal = []
listAtt30Key = []
listAtt30Val = []
listAtt34Key = []
listAtt34Val = []

targerFolder = input('Enter Path of PCF Files : ')

for file in os.listdir(targerFolder):
    tempFileSpilt = file.split('.')
    lenFileSplit = len(tempFileSpilt)
    tempFileEx = tempFileSpilt[lenFileSplit-1]
    
    if bool(re.match('pcf', tempFileEx)):
        targetFiles.append(os.path.join(targerFolder, file))

for tagerFile in targetFiles:
    with open(tagerFile, 'r', encoding="utf-8") as file:
        lines = file.readlines()
        line = ''
        iA = 0
        iB = 0
        iC = 0

        for line in lines:
            lineSplit = re.split('\s+', line)
            if lineSplit[0] == 'PIPELINE-REFERENCE':
                pcfRefKey = lineSplit[0]
                pcfRefVal = lineSplit[1]
                iA = 1
            if lineSplit[1] == 'ATTRIBUTE30':
                pcfAtt30Key = lineSplit[1]
                pcfAtt30Val = lineSplit[2]
                iB = 1
            if lineSplit[1] == 'ATTRIBUTE34':
                pcfAtt34Key = lineSplit[1]
                pcfAtt34Val = lineSplit[2]
                iC = 1
            if iA == 1 and iB == 1 and iC == 1:
                listRefKey.append(pcfRefKey)
                listRefVal.append(pcfRefVal)
                listAtt30Key.append(pcfAtt30Key)
                listAtt30Val.append(pcfAtt30Val)
                listAtt34Key.append(pcfAtt34Key)
                listAtt34Val.append(pcfAtt34Val)
                break

            


data = {'RefKey': listRefKey,
        'RefVal': listRefVal,
        'Att30Key': listAtt30Key,
        'Att30Val': listAtt30Val,
        'Att34Key': listAtt34Key,
        'Att34Val': listAtt34Val}
pcfDF = DataFrame(data)
pcfDF