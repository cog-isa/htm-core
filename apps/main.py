from spatialPooler import sp_settings
from spatialPooler.mappers.sp_very_simple_mapper import VerySimpleMapper
from spatialPooler.sp_region import Region
from spatialPooler.spooler import SpatialPooler
import temporalPooler.htm__region as tp
from apps.settings import *


def toVector(m):
    output=[]
    for i in m:
        for j in i:
            output.append(j)
    return output


def toMatrix(region):
    return [[region.get_columns()[j*region.get_col_h() + i].get_is_active() for i in range(region.get_col_h())] for j in range(region.get_col_w())]

generator = MakeBubble(GENERATOR, REGION_SIZE_N, SCALE)

setting = sp_settings.HTMSettings.get_default_settings()
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

r = Region(setting,VerySimpleMapper())
r_t = tp.Region(setting.xDimension, setting.cellsPerColumn)
sp = SpatialPooler(setting)

for i in range(STEPS_NUMBER):
    inp=toVector(generator.get_data())
    # generator.out()

    ov=sp.update_overlaps(r.get_columns(), inp)
    sp.inhibition_phase(r.get_columns(), ov)
    # sp.learning_phase(r.get_columns(), inp, ov)

    inp_t=toMatrix(r)

    for j in inp_t:
        print(j)

    r_t.step_forward(inp_t)
    r_t.out_prediction()
    generator.move()
