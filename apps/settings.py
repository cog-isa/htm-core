from gens.input_generators import *

# раздувание
SCALE = 3

REGION_SIZE_N = 3

# количество клеток в колонке
COLUMN_SIZE = 3

STEPS_NUMBER = 50000

# GENERATOR = HardSteps
# GENERATOR = ConstantActiveBit
# GENERATOR = TestSimpleSteps
GENERATOR = TestSimpleSteps

INITIAL_PERMANENCE = 0.30
SYNAPSE_THRESHOLD = 0.25
DENDRITE_PERMANENCE_INC_DELTA = 0.02
DENDRITE_PERMANENCE_DEC_DELTA = -0.1
DENDRITE_ACTIVATE_THRESHOLD = 1
PASSIVE_TIME_TO_ACTIVE_THRESHOLD = 2000



