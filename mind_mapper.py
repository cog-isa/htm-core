__author__ = 'tv'

from spatialPooler.mappers.sp_square_mapper_auto_radius import SquareMapperAutoRadius
from gens.input_generators import Cross


def map_to_matrix(mapped, input, output_size):
    res = []
    p =  []
    cnt = 0
    # здесь были костыли
    return res


def get_slices(input, output_size, getter_matrix):
    input_size = len(input)
    for i, e in enumerate(getter_matrix):
        for j, elem in enumerate(e):
            if elem:
                print(
                    map_to_matrix(SquareMapperAutoRadius.get_columns_cells_by_coord(i, j, input_size, output_size, 1),
                    input))


if __name__ == "__main__":
    generator = Cross(10)
    vision = [[1, 0], [0, 1]]
    get_slices(generator.get_data(), len(vision), vision)
