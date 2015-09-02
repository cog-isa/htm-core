from gens.input_generators import *


class TemporalSettings:

    def __init__(self):
        # раздувание
        self.SCALE = 3

        self.REGION_SIZE_N = 3

        # количество клеток в колонке
        self.COLUMN_SIZE = 3

        self.STEPS_NUMBER = 50000

        # GENERATOR = HardSteps
        # GENERATOR = ConstantActiveBit
        # GENERATOR = TestSimpleSteps
        self.GENERATOR = TestSimpleSteps

        self.INITIAL_PERMANENCE = 0.30
        self.SYNAPSE_THRESHOLD = 0.25
        self.DENDRITE_PERMANENCE_INC_DELTA = 0.02
        self.DENDRITE_PERMANENCE_DEC_DELTA = -0.1
        self.DENDRITE_ACTIVATE_THRESHOLD = 1
        self.PASSIVE_TIME_TO_ACTIVE_THRESHOLD = 2000

class SpatialSettings:

    def __init__(self):
        self.debug = False
        self.activation_threshold = 1
        self.min_overlap = 1
        self.desired_local_activity = 3
        self.connected_pct = 1
        self.connected_perm = 0.01
        self.xinput = 0
        self.yinput = 0
        self.potential_radius = 4
        self.xdimension = 10
        self.ydimension = 10
        self.initial_inhibition_radius = 1
        self.permanence_inc = 0.1
        self.permanence_dec = 0.1
        self.cells_per_column = 2
        self.max_boost = 1
        self.debug = True
        self.min_duty_cycle_fraction = 2

temporal_settings = TemporalSettings()
spatial_settings = SpatialSettings()
