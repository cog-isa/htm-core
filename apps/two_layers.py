from spatialPooler.mappers.sp_square_mapper import SquareMapper
from spatialPooler.utils import to_binmatrix
import temporalPooler.htm__region as tp
import spatialPooler.sp_region as sp
from apps.settings import *

generator = MakeBubble(input_settings.GENERATOR, temporal_settings.REGION_SIZE_N, input_settings.SCALE)


spatial_settings.yinput=spatial_settings.xinput*input_settings.SCALE
spatial_settings.xinput=spatial_settings.xinput*input_settings.SCALE
spatial_settings.ydimension=spatial_settings.xdimension

r1_s = sp.Region(spatial_settings, input_settings.MAPPER)
r1_t = tp.Region(spatial_settings.xdimension, temporal_settings.COLUMN_SIZE)

spatial_settings2=SpatialSettings()
spatial_settings2.yinput=spatial_settings.xdimension
spatial_settings2.xinput=spatial_settings.xdimension
spatial_settings2.xdimension=spatial_settings2.ydimension=3
r2_s = sp.Region(spatial_settings2, input_settings.MAPPER)
r2_t = tp.Region(spatial_settings2.xdimension, temporal_settings.COLUMN_SIZE)

for i in range(input_settings.STEPS_NUMBER):
    print('GenData')
    inp_t = r1_s.step_forward(generator.get_data())
    generator.out()
    print('SP1')
    for j in inp_t:
        print(j)
    r1_t.step_forward(inp_t)
    print('TP1')
    # r1_t.out_prediction()

    inp2_t = r2_s.step_forward(to_binmatrix(inp_t))
    print('SP2')
    for j in inp2_t:
        print(j)
    r2_t.step_forward(inp2_t)
    print('TP2')
    r2_t.out_prediction()
    generator.move()
