from htm__region import Region
from settings import *

generator = GENERATOR(REGION_SIZE_N)

r = Region(REGION_SIZE_N, COLUMN_SIZE)

for i in range(STEPS_NUMBER):
    print('---------------------')
    generator.out()
    r.step_forward(generator.get_data())
    r.out_prediction()
    generator.move()
