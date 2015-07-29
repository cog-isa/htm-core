# -*- coding: utf8 -*-
import random

from Cell import Cell
from Synapse import Synapse
from utils import getDistance

__author__ = 'AVPetrov'


class Column:
    def __init__(self,coords, bottomIndices, region):
        self.setting = region.setting;
        self.bottomIndices=bottomIndices;
        self.potentialRadius= self.setting.potentialRadius;
        self.connectedPct= self.setting.connectedPct;
        self.r=region;
        self.isActive=False;
        self.neighbors=[]
        self.col_coords=coords;
        self.cells=[Cell(0) for i in range(0,self.setting.cellsPerColumn+1)]
        # хэш синапсов: индекс элемента с которым соединение и сам синапс
        self.potentialSynapses ={}
        self.boostFactor = 1;
        self.rand = random.Random()
        self.rand.seed = 1
        self.initSynapses()
        self.updateNeighbors(self.setting.initialInhibitionRadius)

    def getIndex(self):
        return self.col_coords[0]*self.setting.yDimension+self.col_coords[1];

    # /**
    #  * Изменение списка соседних колонок, которые отстоят от данной в круге радиусом inhibitionRadius
    #  * @param inhibitionRadius радиус подавления (в начале назначется из настроек, потом берется как усредненный радиус рецептивного поля)
    #  */
    def updateNeighbors(self,inhibitionRadius):
        self.neighbors=[]
        for k in range(self.col_coords[0] - inhibitionRadius,self.col_coords[0] + inhibitionRadius+1):
            if k >= 0 and k < self.setting.xDimension:
                for m in range(self.col_coords[1] - inhibitionRadius,self.col_coords[1] + inhibitionRadius+1):
                    if m >= 0 and m < self.setting.yDimension:
                        if k!=self.col_coords[0] or m!=self.col_coords[1]:
                            self.neighbors.append(k * self.setting.yDimension + m);

    def getNeighbors(self):
        return self.neighbors;


    def setIsActive(self,isActive):
        self.isActive=isActive;

    def isActive(self):
        return self.isActive;


    def getCoord(self):
        return self.col_coords;


    def getPotentialSynapses(self):
        return self.potentialSynapses;


    def getConnectedSynapses(self):
        conn_syn=[]
        for s in self.potentialSynapses.values():
            if s.isConnected():
                conn_syn.append(s)
        return conn_syn

    def getBoostFactor(self):
        return self.boostFactor;


    def setBoostFactor(self,boostFactor):
        self.boostFactor = 1;


    def stimulate(self):
        for synapse in self.potentialSynapses.values():
            synapse.increasePermanence();



    def initSynapses(self):
        center = self.bottomIndices[len(self.bottomIndices)//2]

        if self.setting.debug==False:
            self.rand.shuffle(self.bottomIndices)

        # // выберем только часть синапсов для данной колонки (если set.connectedPct<1)
        # // предполагается, что set.connectedPct<1, в том случае, если рецептивные поля различных колонок пересекаются
        numPotential = round(len(self.bottomIndices) * self.connectedPct);
        for i in range(0,numPotential):
            coord = self.bottomIndices[i]
            index= coord[0]*self.setting.yInput+coord[1]
            synapse = Synapse(self.setting, index, 0)
            # //радиальное затухание перманентности от центра рецептивного поля колонки
            # //double k = MathUtils.distFromCenter(index, set.potentialRadius, set.xDimension, set.yDimension);
            k = getDistance (coord,center )
            synapse.initPermanence(k)
            self.potentialSynapses[index]=synapse