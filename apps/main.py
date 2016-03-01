from gens.input_generators import Cross
from gens.make_bubble import MakeBubble
from temporalPooler.htm__region import Region as TemporalPoolerRegion
from apps.settings import *

size = 12
temporal_settings = TemporalSettings(region_size=size, column_size=4, initial_permanence=0.5,
                                     dendrite_activate_threshold=8, dendrite_permanence_inc_delta=0.02,
                                     dendrite_permanence_dec_delta=-0.1, passive_time_to_active_threshold=1000,
                                     synapse_threshold=0.45)
generator = MakeBubble(Cross, size // 4, 4)

temporal_pooler_region = TemporalPoolerRegion(temporal_settings=temporal_settings)

for i in range(700):
    generator.out()
    temporal_pooler_region.step_forward(generator.get_data())
    temporal_pooler_region.out_prediction()
    generator.move()
