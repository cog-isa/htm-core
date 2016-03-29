from apps.settings import TemporalSettings
from gens.make_bubble import MakeBubble
from gens import input_generators
from temporalPooler.htm__region import Region


class Foo:
    def __init__(self, pre_learning_steps):
        self.generator = MakeBubble(input_generators.H3, 2, 1)
        tp_level_one_settings = TemporalSettings(region_size=2, column_size=4, initial_permanence=0.5,
                                                 dendrite_activate_threshold=1, dendrite_permanence_inc_delta=0.02,
                                                 dendrite_permanence_dec_delta=-0.1,
                                                 passive_time_to_active_threshold=1000,
                                                 synapse_threshold=0.45)
        self.tp_level_one = Region(tp_level_one_settings)
        for i in range(pre_learning_steps):
            self.tp_level_one.step_forward(self.generator.get_data())
            self.tp_level_one.out_prediction()
            self.generator.move()

        # замораживаем состояние региона
        tp_level_one_settings.dendrite_permanence_dec_delta = tp_level_one_settings.dendrite_permanence_inc_delta = 0.0
        tp_level_one_settings.passive_time_to_active_threshold=10000000000000000000

        dendrite_id_cnt = 0
        self.id_to_dendrite_map = {}
        self.id_to_Cell = {}
        self.dendrites = []
        for i, I in enumerate(self.tp_level_one.columns):
            for j, J in enumerate(I):
                for cell, Cell in enumerate(self.tp_level_one.columns[i][j].cells):
                    self.id_to_Cell[Cell.id] = Cell
                    Cell.position_x_y = [i, j]
                    for dendrite, Dendrite in enumerate(Cell.dendrites):
                        self.dendrites.append(Dendrite)
                        Dendrite.id = dendrite_id_cnt
                        Dendrite.id_to = Cell.id
                        dendrite_id_cnt += 1
                        Dendrite.position_x_y = [i, j]
                        self.id_to_dendrite_map[Dendrite.id] = Dendrite


def main():
    Foo(100)


if __name__ == "__main__":
    main()