from gens.combine_gens import StepsAndCross
from gens.input_generators import TestSimpleSteps
from spatialPooler.mappers.sp_square_mapper_auto_radius import SquareMapperAutoRadius


class InputSettings:
    def __init__(self):
        # раздувание
        self.SCALE = 1
        self.STEPS_NUMBER = 700
        self.MAPPER = SquareMapperAutoRadius


class TemporalSettings:
    # статическое поле, используется для предотвращения пересечений id клеток в разных регионах
    free_id = 0

    def __init__(self, region_size, column_size, initial_permanence, synapse_threshold, dendrite_permanence_inc_delta,
                 dendrite_permanence_dec_delta, dendrite_activate_threshold, passive_time_to_active_threshold):
        self.region_size = region_size
        self.column_size = column_size
        self.initial_permanence = initial_permanence
        self.synapse_threshold = synapse_threshold
        self.dendrite_permanence_inc_delta = dendrite_permanence_inc_delta
        self.dendrite_permanence_dec_delta = dendrite_permanence_dec_delta
        self.dendrite_activate_threshold = dendrite_activate_threshold
        self.passive_time_to_active_threshold = passive_time_to_active_threshold


class SpatialSettings:
    def __init__(self):
        self.debug = False
        self.min_overlap = 1
        self.desired_local_activity = 4
        self.connected_pct = 1
        self.connected_perm = 0.01
        self.xinput = 3
        self.yinput = 3
        self.potential_radius = 4
        self.xdimension = 3
        self.ydimension = 3
        self.initial_inhibition_radius = 1
        self.permanence_inc = 0.1
        self.permanence_dec = 0.1
        self.max_boost = 2
        self.min_duty_cycle_fraction = 0.2
