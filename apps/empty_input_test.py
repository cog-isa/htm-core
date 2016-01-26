import temporalPooler.htm__region as tp
from apps.settings import *
from hierarchy.CombinedGenerator import CombineGenerator
from hierarchy.util import zip_binary_matrix, unzip_binary_matrix


tss1 = TestSimpleSteps(3)
tss1.move()
tss2 = TestSimpleSteps(3)
tss2.move()

generator = CombineGenerator([tss1, tss2])
input_size = len(generator.empty)

r_t = tp.Region(input_size, 4)

for i in range(input_settings.STEPS_NUMBER):
    data = generator.get_data()
    generator.out()
    r_t.step_forward(data)
    r_t.out_prediction()
    generator.move()


ones = [[1 for x in range(6)] for x in range(6)]

r_t.step_forward(generator.empty)
r_t.out_prediction()

r_t.step_forward(ones)
r_t.out_prediction()

r_t.step_forward(generator.empty)
r_t.out_prediction()

r_t.step_forward(ones)
r_t.out_prediction()