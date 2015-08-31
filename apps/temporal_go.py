from temporalPooler.htm__region import Region
from apps.settings import temporal_settings
from gens.input_generators import MakeBubble

generator = MakeBubble(temporal_settings.GENERATOR, temporal_settings.REGION_SIZE_N,
                                         temporal_settings.SCALE)

r = Region(temporal_settings.REGION_SIZE_N * temporal_settings.SCALE, temporal_settings.COLUMN_SIZE)
print("""
**** ЛЕГЕНДА *****
P1 - Клетка с номером 1, данной колонки находится в состоянии предсказания
A3 - Клетка с номером 3, данной колонки активировалась
O3 - Клетка с номером 3, данной колонки активировалась из-за  простоя (PassiveTime > PASSIVE_TIME_TO_ACTIVE_THRESHOLD)
""")

for i in range(temporal_settings.STEPS_NUMBER):
    print('---------------------')
    # generator.out()
    r.step_forward(generator.get_data())
    r.out_prediction()
    generator.move()
