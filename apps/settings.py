from gens.combine_gens import StepsAndCross
from gens.input_generators import TestSimpleSteps
from spatialPooler.mappers.sp_square_mapper_auto_radius import SquareMapperAutoRadius


class InputSettings:
    def __init__(self, SCALE, STEPS_NUMBER):
        # раздувание
        self.SCALE = SCALE #1
        self.STEPS_NUMBER = STEPS_NUMBER #700


class TemporalSettings:
    # статическое поле, используется для предотвращения пересечений id клеток в разных регионах
    free_id = 0

    def __init__(self, region_size, column_size, initial_permanence, synapse_threshold, dendrite_permanence_inc_delta,
                 dendrite_permanence_dec_delta, dendrite_activate_threshold, passive_time_to_active_threshold):
        self.region_size = region_size
        # Количество клеток в колонке
        self.column_size = column_size
        # Начальная перманентность синапса
        self.initial_permanence = initial_permanence
        # Если перманентность синапса выше этой велечины, он будет срабатывать
        self.synapse_threshold = synapse_threshold
        # Значение, которое будет прибавляться к перманентности синапсов дендрита, которые привели к правильному предсказанию
        self.dendrite_permanence_inc_delta = dendrite_permanence_inc_delta
        # Значение, которое будет прибавляться к перманентности синапсов дендрита, которые привели к неправильному предсказанию
        self.dendrite_permanence_dec_delta = dendrite_permanence_dec_delta
        # Необходимое количество активных синапсов для активации дендрита
        self.dendrite_activate_threshold = dendrite_activate_threshold
        # Порог, определяющий активацию клетки, даже если она не была предсказана (долго простаивала)
        self.passive_time_to_active_threshold = passive_time_to_active_threshold


class SpatialSettings:


    def __init__(self, debug, min_overlap, desired_local_activity, connected_pct, connected_perm, xinput, yinput,
                 potential_radius, xdimension, ydimension, initial_inhibition_radius, permanence_inc, permanence_dec,
                 max_boost, min_duty_cycle_fraction):
        self.debug = False
        self.min_overlap = min_overlap #1
        self.desired_local_activity = desired_local_activity #4
        self.connected_pct = connected_pct #1
        self.connected_perm = connected_perm #0.01
        self.xinput = xinput #3
        self.yinput = yinput #3
        self.potential_radius = potential_radius# 4
        self.xdimension = xdimension #3
        self.ydimension = ydimension #3
        self.initial_inhibition_radius = initial_inhibition_radius #1
        self.permanence_inc = permanence_inc #0.1
        self.permanence_dec = permanence_dec #0.1
        self.max_boost = max_boost #2
        self.min_duty_cycle_fraction = min_duty_cycle_fraction #0.2
