from spatialPooler.mappers.sp_square_mapper import SquareMapper
import temporalPooler.htm__region as tp
import spatialPooler.sp_region as sp
from apps.settings import *

generator = MakeBubble(input_settings.GENERATOR, temporal_settings.REGION_SIZE_N, input_settings.SCALE)


spatial_settings.yinput=spatial_settings.xinput*input_settings.SCALE
spatial_settings.xinput=spatial_settings.xinput*input_settings.SCALE
spatial_settings.ydimension=spatial_settings.xdimension

r_s = sp.Region(spatial_settings, input_settings.MAPPER)
r_t = tp.Region(spatial_settings.xdimension, temporal_settings.COLUMN_SIZE)

for i in range(input_settings.STEPS_NUMBER):
    data=generator.get_data()
    generator.out()
    inp_t = r_s.step_forward(data)
    for j in inp_t:
        print(j)
    r_t.step_forward(inp_t)
    r_t.out_prediction()
    generator.move()
