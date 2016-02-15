from gens.make_bubble import MakeBubble
from temporalPooler.htm__region import Region as TemporalPoolerRegion
from apps.settings import *

temporal_settings = TemporalSettings(region_size=4, column_size=4, initial_permanence=0.5,
                                     dendrite_activate_threshold=1, dendrite_permanence_inc_delta=0.02,
                                     dendrite_permanence_dec_delta=-0.1, passive_time_to_active_threshold=1000,
                                     synapse_threshold=0.45)
input_settings = InputSettings(SCALE=1, STEPS_NUMBER=700, MAPPER=SquareMapperAutoRadius)
generator = MakeBubble(TestSimpleSteps, temporal_settings.region_size, input_settings.SCALE)
temporal_pooler_region = TemporalPoolerRegion(temporal_settings=temporal_settings)

for i in range(input_settings.STEPS_NUMBER):
    generator.out()
    temporal_pooler_region.step_forward(generator.get_data())
    temporal_pooler_region.out_prediction()
    generator.move()
