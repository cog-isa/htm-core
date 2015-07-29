import random

from Cell import Cell
from Synapse import Synapse
from utils import getDistance

__author__ = 'AVPetrov'


class Column:
    def __init__(self,coords, bottomIndices, region, set):
        self.set = set;
        self.bottomIndices=bottomIndices;
        self.potentialRadius= set.potentialRadius;
        self.connectedPct= set.connectedPct;
        self.r=region;
        self.isActive=False;
        self.neighbors=[]
        self.col_coords=coords;
        self.cells=[Cell(0) for i in range(0,set.cellsPerColumn)]
        # ��� ��������: ������ �������� � ������� ���������� � ��� ������
        self.potentialSynapses ={}
        self.boostFactor = 1;
        self.rand = random.Random()
        self.rand.seed = 1
        self.initSynapses()
        self.updateNeighbors(self.set.initialInhibitionRadius)

    def getIndex(self):
        return self.col_coords.getX()*self.set.yDimension+self.col_coords.getY();

    # /**
    #  * ��������� ������ �������� �������, ������� ������� �� ������ � ����� �������� inhibitionRadius
    #  * @param inhibitionRadius ������ ���������� (� ������ ���������� �� ��������, ����� ������� ��� ����������� ������ ������������ ����)
    #  */
    def updateNeighbors(self,inhibitionRadius):
        neighbors=[]
        for k in range(self.col_coords[0] - inhibitionRadius,self.col_coords[0] + inhibitionRadius):
            if k >= 0 and k < set.xDimension:
                for m in range(self.col_coords[1] - inhibitionRadius,self.col_coords[1] + inhibitionRadius):
                    if m >= 0 and m < set.yDimension:
                        if k!=self.col_coords[0] or m!=self.col_coords[1]:
                            neighbors.add(k * set.yDimension + m);

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
                conn_syn.add(s)
        return conn_syn

    def getBoostFactor(self):
        return self.boostFactor;


    def setBoostFactor(self,boostFactor):
        self.boostFactor = 1;


    def stimulate(self):
        for synapse in self.potentialSynapses.values():
            synapse.increasePermanence();



    def initSynapses(self):
        center = self.bottomIndices[len(self.bottomIndices)/2]

        if self.set.debug==False:
            self.rand.shuffle(self.bottomIndices)

        # // ������� ������ ����� �������� ��� ������ ������� (���� set.connectedPct<1)
        # // ��������������, ��� set.connectedPct<1, � ��� ������, ���� ����������� ���� ��������� ������� ������������
        numPotential = round(self.bottomIndices.size() * self.connectedPct);
        for i in range(0,numPotential):
            coord = self.bottomIndices[i]
            index= coord[0]*self.set.yInput+coord[1]
            synapse = Synapse(set, index)
            # //���������� ��������� �������������� �� ������ ������������ ���� �������
            # //double k = MathUtils.distFromCenter(index, set.potentialRadius, set.xDimension, set.yDimension);
            k = getDistance (coord,center )
            synapse.initPermanence(k)
            self.potentialSynapses.put(index,synapse)