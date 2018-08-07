import re
import os
from pandas import DataFrame as df, ExcelWriter


targetFiles = []
listRefVal = []
listAtt30Val = []
listAtt34Val = []
listSuptNameVal = []
listSuptUciVal = []
listSuptMtlVal = []

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
            pcfRefVal = ""
            pcfAtt30Val = ""
            pcfAtt34Val = ""
            pcfSuptName = ""
            pcfSuptUci = ""
            pcfSuptMtlList = ""

            for line in lines:
                lineSplit = re.split('\s+', line)
                if lineSplit[0] == 'PIPELINE-REFERENCE':
                    pcfRefVal = line[21:].strip()
                    iA = 1
                if lineSplit[1] == 'ATTRIBUTE30':
                    pcfAtt30Val = line[18:].strip()
                if lineSplit[1] == 'ATTRIBUTE34':
                    pcfAtt34Val = line[18:].strip()
                if iB == 1 and line[:7] == "SUPPORT":
                    listRefVal.append(pcfRefVal)
                    listAtt30Val.append(pcfAtt30Val)
                    listAtt34Val.append(pcfAtt34Val)
                    listSuptNameVal.append(pcfSuptName)
                    listSuptUciVal.append(pcfSuptUci)
                    listSuptMtlVal.append(pcfSuptMtlList)
                    pcfSuptName = ""
                    pcfSuptUci = ""
                    pcfSuptMtlList = ""
                    iB=1
                elif lineSplit[0] ==  'SUPPORT':
                    iB = 1
                elif iB == 1 and line[:4] == "    ":
                    if lineSplit[1] == 'NAME':
                        pcfSuptName = line[12:].strip()
                    if lineSplit[1] == 'UCI':
                        pcfSuptUci = line[11:].strip()
                    if lineSplit[1] == "MATERIAL-LIST":
                        pcfSuptMtlList = line[21:].strip()
                elif iB == 1 and line[:7] != "SUPPORT":
                    listRefVal.append(pcfRefVal)
                    listAtt30Val.append(pcfAtt30Val)
                    listAtt34Val.append(pcfAtt34Val)
                    listSuptNameVal.append(pcfSuptName)
                    listSuptUciVal.append(pcfSuptUci)
                    listSuptMtlVal.append(pcfSuptMtlList)
                    pcfSuptName = ""
                    pcfSuptUci = ""
                    pcfSuptMtlList = ""
                    iB=0
                else:
                    iB=0
                


            if iA == 0:
                print('레퍼런스 ID가 없는 {} 파일이 존재합니다.'.format(tagerFile))
                break


except Exception :
    print('{} 파일에서 에러가 났어요.'.format(tagerFile))


data = {'SUPPORT NAME': listSuptNameVal,            #input excel coulumn name
        'SUPPORT UCI': listSuptUciVal,              #input excel coulumn name
        'SUPPORT MATERIAL LIST': listSuptMtlVal,    #input excel coulumn name
        'WBS ISO': listRefVal,                      #input excel coulumn name
        'ATTRIBUTE30': listAtt30Val,                #input excel coulumn name
        'ATTRIBUTE34': listAtt34Val}                #input excel coulumn name
pcfDF = df(data)
writer = ExcelWriter('PCF_output.xlsx')
pcfDF.to_excel(writer,'PCF',index=False)
writer.save()
print("완료")
