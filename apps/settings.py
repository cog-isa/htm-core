from gens.input_generators import *
from spatialPooler.mappers.sp_square_mapper_auto_radius import SquareMapperAutoRadius


class InputSettings:
    def __init__(self):
        # раздувание
        self.SCALE = 1
        self.STEPS_NUMBER = 900

        # GENERATOR = HardSteps
        # GENERATOR = ConstantActiveBit
        # GENERATOR = TestSimpleSteps
        self.GENERATOR = TestSimpleSteps
        self.MAPPER = SquareMapperAutoRadius


class TemporalSettings:
    def __init__(self):
        # раздувание
        self.REGION_SIZE_N = 3

        # количество клеток в колонке
        self.COLUMN_SIZE = 4

        self.INITIAL_PERMANENCE = 0.30
        self.SYNAPSE_THRESHOLD = 0.25
        self.DENDRITE_PERMANENCE_INC_DELTA = 0.02
        self.DENDRITE_PERMANENCE_DEC_DELTA = -0.1
        self.DENDRITE_ACTIVATE_THRESHOLD = 1
        self.PASSIVE_TIME_TO_ACTIVE_THRESHOLD = 2000


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


input_settings = InputSettings()
temporal_settings = TemporalSettings()
spatial_settings = SpatialSettings()
