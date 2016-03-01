from apps.settings import TemporalSettings
from gens.make_bubble import MakeBubble
from gens import input_generators


def main():
    generator = MakeBubble(input_generators.H3, 2, 1)
    tp_l1_settings = TemporalSettings(region_size=2, column_size=2, initial_permanence=0.3, synapse_threshold=0.25,
                                      dendrite_permanence_inc_delta=0.02, dendrite_permanence_dec_delta=-0.1,
                                      dendrite_activate_threshold=, passive_time_to_active_threshold=200)

    pass


if __name__ == "__main__":
    main()