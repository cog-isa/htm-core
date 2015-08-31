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
    pass

temporal_settings = TemporalSettings()
spatial_settings = SpatialSettings()