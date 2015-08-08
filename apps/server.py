import socket
import pickle
import HTMSettings
from htm__region import Region
from mappers.VerySimpleMapper import verySimpleMapper
from region import Region
from socketModule import socketModule
from spatialPooler import SpatialPooler
import temporalPooler.htm__region as tp

__author__ = 'AVPetrov'

# реализует ответ на запрос - Дай состояние и сделай шаг вперед
from settings import *

def handle(data,answer):
    if(data.decode('utf-8')):
        return pickle.dumps(answer, pickle.HIGHEST_PROTOCOL)
    else:
        return "UNKNOW REQUEST"

server=socketModule()
server.openLocalPort(11101)




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
setting.xDimension = 1
setting.yDimension = 1
setting.initialInhibitionRadius=1
setting.cellsPerColumn=5


r = Region(setting,verySimpleMapper())
r_t=tp.Region(setting.xDimension, setting.cellsPerColumn)
sp=SpatialPooler(setting)

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
    server.waitForRqst(lambda data: handle(data,r_t))
