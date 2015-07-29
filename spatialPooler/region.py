import sys
from Column import Column

__author__ = 'AVPetrov'


class Region:
    def __init__(self,setting,mapper):
        self.mapper=mapper;
        self.columns=[];
        self.setting=setting;
        bottomIndices=[]
        try:
            bottomIndices = mapper.mapAll((self.setting.xInput, self.setting.yInput), (self.setting.xDimension, self.setting.yDimension), self.setting.potentialRadius);
        except:
           print("Unexpected error:", sys.exc_info()[0])

        for i in range(self.setting.xDimension):
            for j in range(self.setting.yDimension):
                self.columns.append((Column((i, j), bottomIndices[i*self.setting.yDimension+j], self)));

        return

    def getColumns(self):
        return self.columns;
    def getInputW(self):
        return self.settings.xInput
    def getInputH(self):
        return self.settings.yInput;