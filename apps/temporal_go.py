# пробуем добавить settings, если они не добавлены - добавляем
# такие грабли нужны для корректного отображения в ide
try:
    from apps.settings import *
except ValueError and SystemError:
    pass

from temporalPooler.htm__region import Region
from gens.input_generators import MakeBubble

# generator = GENERATOR(REGION_SIZE_N)

generator = MakeBubble(GENERATOR, REGION_SIZE_N, SCALE)

r = Region(REGION_SIZE_N * SCALE, COLUMN_SIZE)
print("""
**** ЛЕГЕНДА *****
P1 - Клетка с номером 1, данной колонки находится в состоянии предсказания
A3 - Клетка с номером 3, данной колонки активировалась
O3 - Клетка с номером 3, данной колонки активировалась из-за  простоя (PassiveTime > PASSIVE_TIME_TO_ACTIVE_THRESHOLD)
""")

for i in range(STEPS_NUMBER):
    print('---------------------')
    # generator.out()
    r.step_forward(generator.get_data())
    r.out_prediction()
    generator.move()
