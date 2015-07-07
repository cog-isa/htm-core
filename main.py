from htm__region import Region
from input_generators import TestSimpleSteps, TooTestSimpleSteps
SZ = 5
COL_SZ = 2

simple_steps = TestSimpleSteps(SZ)

# htm = [[Column(COL_SZ) for jj in range(SZ)] for ii in range(SZ)]


r = Region(SZ, COL_SZ)

# поучимся 30 шагов
for i in range(31):
    print('---------------------')

    r.step_forward(simple_steps.get_data())

    r.out_prediction()
    simple_steps.out()

    simple_steps.move()














