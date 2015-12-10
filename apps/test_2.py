import spatialPooler.sp_region as sp

import temporalPooler.htm__region as tp
from apps.settings import *
from gens.input_generators import Cross, TestSimpleSteps
from mind_vision_experiment.merge_inputs import merge_input
spatial_settings.yinput = spatial_settings.xinput * input_settings.SCALE
spatial_settings.xinput = spatial_settings.xinput * input_settings.SCALE
spatial_settings.ydimension = spatial_settings.xdimension


r_t = tp.Region(6, 4)

T = 8

class OloloGenerator:
    def __init__(self):
        self.cnt = 0
        self.gen1 = TestSimpleSteps(3)
        self.gen1.move()
        self.gen2 = TestSimpleSteps(3)

    def move(self):
        if self.cnt < T:
            self.gen1.move()
        if self.cnt >= T:
            self.gen2.move()
        if self.cnt == T + 7:
            self.cnt = 0
        self.cnt += 1

    def get_data(self):
        get1 = self.gen1.get_data()
        get2 = self.gen2.get_data()
        if self.cnt >= T:
            for i in range(3):
                for j in range(3):
                    get1[i][j] = 0
        if self.cnt <= T:
            for i in range(3):
                for j in range(3):
                    get2[i][j] = 0
        return merge_input([get1, get2])


# t = OloloGenerator()
# for i in range(40):
#     t.move()
#     for i in t.get_data():
#         print(i)
#     print()
# exit(0)
#
generator = OloloGenerator()

for i in range(input_settings.STEPS_NUMBER):
    data = generator.get_data()
    # generator.out()
    r_t.step_forward(data)
    r_t.out_prediction()
    generator.move()
