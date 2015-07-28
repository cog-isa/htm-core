import random
from htm_cell import Cell

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
		self.rand.seed = 10

        initSynapses();
        updateNeighbors(self.set.initialInhibitionRadius);

    def getIndex(self):
        return self.col_coords.getX()*Column.this.set.yDimension+self.col_coords.getY();

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
				conn_syn.add(s);
		return  conn_syn;





    def getBoostFactor(self):
        return self.boostFactor;


	def setBoostFactor(self,boostFactor):
        self.boostFactor = 1;


 	def stimulate(self):
		for synapse in self.potentialSynapses.values():
			synapse.increasePermanence();

	def initSynapses():
		center =bottomIndices.get(bottomIndices.size()/2);

            if(HTMSettings.debug==false)
                Collections.shuffle(bottomIndices, random);

            // ������� ������ ����� �������� ��� ������ ������� (���� set.connectedPct<1)
            // ��������������, ��� set.connectedPct<1, � ��� ������, ���� ����������� ���� ��������� ������� ������������
            int numPotential = (int) Math.round(bottomIndices.size() * Column.this.connectedPct);
            for (int i = 0; i < numPotential; i++) {
                Vector2D coord = bottomIndices.get(i);
                int index=(int)coord.getX()*Column.this.set.yInput+(int)coord.getY();
                Synapse synapse = new Synapse(set, index);
                //���������� ��������� �������������� �� ������ ������������ ���� �������
                //double k = MathUtils.distFromCenter(index, set.potentialRadius, set.xDimension, set.yDimension);
                double k = Vector2D.getDistance(coord,center );
                synapse.initPermanence(k);
                potentialSynapses.put(index,synapse);
            }
        }
    }
}