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
        self.activation_threshold = 0
        self.min_overlap = 0
        self.desired_local_activity = 0
        self.connected_pct = 0
        self.connected_perm = 0
        self.xinput = 0
        self.yinput = 0
        self.potential_radius = 0
        self.xdimension = 0
        self.ydimension = 0
        self.initial_inhibition_radius = 0
        self.permanence_inc = 0
        self.permanence_dec = 0
        self.cells_per_column = 0
        self.max_boost = 0
        self.debug = True
        self.min_duty_cycle_fraction = 0

    @staticmethod
    def get_default_settings():
        setting = SpatialSettings()
        setting.activation_threshold = 1
        setting.min_overlap = 1
        setting.desired_local_activity = 3
        setting.connected_pct = 1
        setting.connected_perm = 0.01
        setting.potential_radius = 4
        setting.xdimension = 10
        setting.ydimension = 10
        setting.initial_inhibition_radius = 1
        setting.permanence_inc = 0.1
        setting.permanence_dec = 0.1
        setting.cells_per_column = 2
        setting.min_duty_cycle_fraction = 2
        setting.max_boost = 1
        setting.debug = True
        return setting

temporal_settings = TemporalSettings()
spatial_settings = SpatialSettings()
