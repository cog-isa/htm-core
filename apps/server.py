import socket
import pickle
import HTMSettings
from htm__region import Region
from mappers.VerySimpleMapper import verySimpleMapper
from region import Region
from spatialPooler import SpatialPooler
import temporalPooler.htm__region as tp

__author__ = 'AVPetrov'

# реализует ответ на запрос - Дай состояние и сделай шаг вперед

from settings import *

SOCKET_PORT = 11101

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', SOCKET_PORT)
sock.bind(server_address)
sock.listen(1)

while True:
    connection, client_address = sock.accept()
    data = ""
    data += connection.recv(512).decode('utf-8')
    # connection.close()
    end_message = "[THIS_IS_THE_END_HOLD_YOUR_BREATH_AND_COUNT_TO_TEN]"
    print(data)
    if data.find('get:') != -1:
        data=pickle.dumps(tp.Region(3,3), pickle.HIGHEST_PROTOCOL)
        connection.sendall(data)
        connection.sendall(bytes(end_message, 'UTF-8'))
        connection.close()


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
