import re
import os
from pandas import DataFrame as df, ExcelWriter


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
    
    if bool(re.match('pcf', tempFileEx, re.IGNORECASE)):
        targetFiles.append(os.path.join(targerFolder, file))

try:
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
                    pcfRefVal = line[21:].strip()
                    iA = 1
                if lineSplit[1] == 'ATTRIBUTE30':
                    pcfAtt30Val = line[18:].strip()
                    iB = 1
                if lineSplit[1] == 'ATTRIBUTE34':
                    pcfAtt34Val = line[18:].strip()
                    iC = 1
                if iA == 1 and iB == 1 and iC == 1:
                    listRefVal.append(pcfRefVal)
                    listAtt30Val.append(pcfAtt30Val)
                    listAtt34Val.append(pcfAtt34Val)
                    break
except Exception :
    print('{} 파일에서 에러가 났어요.'.format(tagerFile))


data = {'WBS ISO': listRefVal,          #input excel coulumn name
        'ATTRIBUTE30': listAtt30Val,    #input excel coulumn name
        'ATTRIBUTE34': listAtt34Val}    #input excel coulumn name
pcfDF = df(data)
writer = ExcelWriter('PCF_output.xlsx')
pcfDF.to_excel(writer,'PCF',index=False)
writer.save()
print("완료")