from spatialPooler.mappers.sp_square_mapper import SquareMapper
import temporalPooler.htm__region as tp
import spatialPooler.sp_region as sp
from apps.settings import *

generator = MakeBubble(input_settings.GENERATOR, temporal_settings.REGION_SIZE_N, input_settings.SCALE)

setting = spatial_settings

setting.xinput = temporal_settings.REGION_SIZE_N * input_settings.SCALE
setting.yinput = temporal_settings.REGION_SIZE_N * input_settings.SCALE
setting.xdimension = temporal_settings.REGION_SIZE_N * input_settings.SCALE
setting.ydimension = temporal_settings.REGION_SIZE_N * input_settings.SCALE

r_s = sp.Region(setting, SquareMapper)
r_t = tp.Region(setting.xdimension, setting.cells_per_column)

for i in range(input_settings.STEPS_NUMBER):

    inp_t=r_s.step_forward(generator.get_data())
    for j in inp_t:
        print(j)
    r_t.step_forward(inp_t)
    r_t.out_prediction()
    generator.move()
