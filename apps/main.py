# from spatialPooler import sp_settings
# from apps.settings import spatial_settings
from spatialPooler.mappers.sp_very_simple_mapper import VerySimpleMapper
from spatialPooler.mappers.sp_square_mapper import SquareMapper
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

generator = MakeBubble(temporal_settings.GENERATOR, temporal_settings.REGION_SIZE_N, temporal_settings.SCALE)

setting = spatial_settings.get_default_settings()
setting.debug = True

setting.activation_threshold = 1
setting.min_overlap = 1
setting.desired_local_activity = 3
setting.connected_pct= 1
setting.xinput = temporal_settings.REGION_SIZE_N*temporal_settings.SCALE
setting.yinput = temporal_settings.REGION_SIZE_N*temporal_settings.SCALE
setting.potential_radius = 1
setting.xdimension = 3
setting.ydimension = 3
setting.initial_inhibition_radius = 2
setting.cells_per_column = 5

r = Region(setting, SquareMapper)
r_t = tp.Region(setting.xdimension, setting.cells_per_column)
sp = SpatialPooler(setting)

for i in range(temporal_settings.STEPS_NUMBER):
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
