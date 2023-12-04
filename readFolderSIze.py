import os
import pandas as pd
import numpy as np

class Folder:
    def __init__(self, absolutePath):
        self.path = absolutePath
        self.child = []
        self.childStatic = []
        self.size = 0
        self.num = 0
        self.finish = False
        
    def getSize(self, folderDict):
        if self.finish == True:
            return self.size
        childNum = len(self.child)
        for i in range(childNum):
            if self.childStatic[i] == 1:
                continue
            self.size += folderDict[self.child[i]].getSize(folderDict)
            self.childStatic[i] = 1
        self.finish = True
        print(self.path, 'size done')
        return self.size

    def addFolder(self, childFolder):
        self.child.append(childFolder)
        self.childStatic.append(0)
        self.num += 1
        self.finish = False

    def addFile(self, filePath):
        self.num += 1
        try:
            size = os.path.getsize(filePath)
        except Exception as e:
            print(filePath, " can't size!!!")
            size = 0
        self.size += size


root = 'C:/'
savePath = './data/C20230817Before.xlsx'
foldersList = []
foldersList.append(root)
folderDict = {}
folder = Folder(root)
folderDict[root] = folder
while len(foldersList) > 0:
    tempRootDir = foldersList[0]
    try:
        files = os.listdir(tempRootDir)
    except Exception as e:
        print(tempRootDir, " can't open!!!!!!!!!!!!!")
        foldersList.pop(0)
        continue
    for filename in files:
        if filename == '.' or filename == '..':
            print('continue:', tempRootDir + '/' + filename)
            continue
        filePath = tempRootDir + '/' + filename
        relativePath = filePath[len(root + '/'):]
        if os.path.isdir(filePath):
            foldersList.append(filePath)
            folder = Folder(filePath)
            folderDict[filePath] = folder
            folderDict[tempRootDir].addFolder(filePath)
            # if len(relativePath.split('/')) < 4:
            #     mainFoldersDict[filePath] = [0, 0]
        else:
            folderDict[tempRootDir].addFile(filePath)
    print(tempRootDir + ' dir end')
    foldersList.pop(0)

folderNum = len(folderDict)
print('folder num:', folderNum)
folderDict[root].getSize(folderDict)

folderInfo = pd.DataFrame(np.arange(folderNum * 3).reshape((folderNum, 3)), columns=['path', 'size', 'num'])
i = 0
for key in folderDict:
    folder = folderDict[key]
    folderInfo['path'][i] = folder.path
    folderInfo['size'][i] = folder.size / 1024 / 1024 #MB
    folderInfo['num'][i] = folder.num
    i += 1
    if i%100 == 0:
        print('i=', i)
folderInfo = folderInfo.sort_values(by='size', ascending=False)
folderInfo.to_excel(savePath, index=False, header=True)