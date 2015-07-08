from htm__region import Region
from input_generators import TestSimpleSteps, TooTestSimpleSteps, Too2TestSimpleSteps, HardSteps
SZ = 3
COL_SZ = 3
simple_steps = HardSteps(SZ)

# htm = [[Column(COL_SZ) for jj in range(SZ)] for ii in range(SZ)]


r = Region(SZ, COL_SZ)

# поучимся 30 шагов
for i in range(513):
    print('---------------------')

    r.step_forward(simple_steps.get_data())

    r.out_prediction()
    simple_steps.out()

    simple_steps.move()














