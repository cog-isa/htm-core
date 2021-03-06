# -*- coding: utf8 -*-
# www.youtube.com/watch?v=IXg_XIm5kqk
from gens.list_images_gen import ListImages
from spatialPooler.mappers.sp_random_mapper import RandomMapper
from spatialPooler.utils import print_matrix, to_binmatrix

__author__ = 'AVPetrov'

from gens.make_bubble import MakeBubble
from temporalPooler.htm__region import Region as TemporalPoolerRegion
from spatialPooler.sp_region import Region as SpatialPoolerRegion
from apps.settings import *

input_settings = InputSettings(SCALE=1, STEPS_NUMBER=300)
generator = ListImages(12)

spatial_settings = SpatialSettings(debug = False, min_overlap = 1, desired_local_activity = 2, connected_pct = 1,
                           connected_perm = 0.1, xinput = generator.square_size, yinput = generator.square_size,
                           potential_radius = 4, xdimension = 12, ydimension = 12, initial_inhibition_radius = 2,
                           permanence_inc = 0.02, permanence_dec = 0.1, max_boost = 2, min_duty_cycle_fraction = 0.2)

temporal_settings = TemporalSettings(region_size=spatial_settings.xdimension, column_size=4, initial_permanence=0.5,
                                     dendrite_activate_threshold=1, dendrite_permanence_inc_delta=0.02,
                                     dendrite_permanence_dec_delta=-0.1, passive_time_to_active_threshold=1000,
                                     synapse_threshold=0.45)


spatial_pooler_region = SpatialPoolerRegion(spatial_settings=spatial_settings, mapper=SquareMapperAutoRadius())
temporal_pooler_region = TemporalPoolerRegion(temporal_settings=temporal_settings)

for i in range(input_settings.STEPS_NUMBER):
    generator.out()
    outdata=spatial_pooler_region.step_forward(generator.get_data())
    print_matrix(to_binmatrix(outdata))
    temporal_pooler_region.step_forward(outdata)
    temporal_pooler_region.out_prediction()
    cols=temporal_pooler_region.columns
    imagined_input = spatial_pooler_region.out_prediction(cols, temporal_settings.region_size)

    generator.move()
