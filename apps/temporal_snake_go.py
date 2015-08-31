import os

from temporalPooler.htm__region import Region
from apps.settings import *

SCALE = 1
generator = Snake(REGION_SIZE_N)

r = Region(REGION_SIZE_N * SCALE, 5)
print("""
**** ЛЕГЕНДА *****
P1 - Клетка с номером 1, данной колонки находится в состоянии предсказания
A3 - Клетка с номером 3, данной колонки активировалась
O3 - Клетка с номером 3, данной колонки активировалась из-за  простоя (PassiveTime > PASSIVE_TIME_TO_ACTIVE_THRESHOLD)
""")

for i in range(STEPS_NUMBER):
    os.system('cls')
    print('---------------------')
    generator.out()
    r.step_forward(generator.get_data())
    r.out_prediction()
    generator.move()
    if generator.game_over:
        generator = Snake(REGION_SIZE_N)
    input()
