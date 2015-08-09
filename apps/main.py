import HTMSettings
from htm__region import Region
from mappers.VerySimpleMapper import verySimpleMapper
from region import Region
from spatialPooler.spooler import SpatialPooler
import temporalPooler.htm__region as tp

__author__ = 'AVPetrov'

from settings import *

def toVector(m):
    output=[]
    for i in m:
        for j in i:
            output.append(j)
    return output

def toMatrix(region):
    return [[region.getColumns()[j*region.getColH() + i].getIsActive() for i in range(region.getColH())] for j in range(region.getColW())]

generator = MakeBubble(GENERATOR, REGION_SIZE_N, SCALE)

setting = HTMSettings.HTMSettings.getDefaultSettings()
setting.debug = True

setting.activationThreshold = 1
setting.minOverlap = 1
setting.desiredLocalActivity = 3
setting.connectedPct = 1
setting.xInput = REGION_SIZE_N*SCALE
setting.yInput = REGION_SIZE_N*SCALE
setting.potentialRadius = 2
setting.xDimension = 5
setting.yDimension = 5
setting.initialInhibitionRadius=2
setting.cellsPerColumn=5




r = Region(setting,verySimpleMapper())
r_t=tp.Region(setting.xDimension, setting.cellsPerColumn)
sp=SpatialPooler(setting)

import pickle

with open('r.pickle', 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(r, f, pickle.HIGHEST_PROTOCOL)

r=0

with open('r.pickle', 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    r = pickle.load(f)

for i in range(STEPS_NUMBER):
    inp=toVector(generator.get_data())
    # generator.out()

    ov=sp.updateOverlaps(r.getColumns(), inp)
    sp.inhibitionPhase(r.getColumns(), ov)
    # sp.learningPhase(r.getColumns(), inp, ov)

    inp_t=toMatrix(r)

    for j in inp_t:
        print(j)

    r_t.step_forward(inp_t)
    r_t.out_prediction()
    generator.move()
