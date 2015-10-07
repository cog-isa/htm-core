from spatialPooler.mappers.sp_square_mapper import SquareMapper
import temporalPooler.htm__region as tp
import spatialPooler.sp_region as sp
from apps.settings import *

generator = MakeBubble(input_settings.GENERATOR, temporal_settings.REGION_SIZE_N, input_settings.SCALE)


spatial_settings.yinput=spatial_settings.xinput*input_settings.SCALE
spatial_settings.xinput=spatial_settings.xinput*input_settings.SCALE
spatial_settings.ydimension=spatial_settings.xdimension

r_s = sp.Region(spatial_settings, SquareMapper)
r_t = tp.Region(spatial_settings.xdimension, temporal_settings.cells_per_column)

for i in range(input_settings.STEPS_NUMBER):
    inp_t = r_s.step_forward(generator.get_data())
    for j in inp_t:
        print(j)
    r_t.step_forward(inp_t)
    r_t.out_prediction()
    generator.move()
