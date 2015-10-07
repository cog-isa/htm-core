from htm__region import Region
from settings import temporal_settings as ts
from gens.input_generators import Cross


def merged_move(regions):
    methods_get_ptr_to_cell = []
    methods_get_active_cells = []
    cells = {}
    active_cells = []
    for i in regions:
        active_cells = active_cells + i.get_active_cells()
        cells.update(i.get_ptr_to_cells())
        methods_get_active_cells.append(i.get_active_cells)
        methods_get_ptr_to_cell.append(i.get_ptr_to_cells)

    for i in regions:
        i.get_ptr_to_cells = lambda: cells
        i.get_active_cells = lambda: active_cells

    for i in regions:
        i.step_forward(Cross(ts.REGION_SIZE_N).get_data())
        i.out_prediction()

    for index, elem in enumerate(regions):
        elem.get_ptr_to_cells = methods_get_ptr_to_cell[index]
        elem.get_active_cells = methods_get_active_cells[index]


if __name__ == "__main__":
    # потестируем
    q = ts.REGION_SIZE_N ** 2 * ts.COLUMN_SIZE
    # важно чтобы id клеток разных регионов не пересекались!!!
    r = [Region(ts.REGION_SIZE_N, ts.COLUMN_SIZE, 0 * (ts.REGION_SIZE_N ** 2 * ts.COLUMN_SIZE)),
         Region(ts.REGION_SIZE_N, ts.COLUMN_SIZE, 1 * (ts.REGION_SIZE_N ** 2 * ts.COLUMN_SIZE)),
         Region(ts.REGION_SIZE_N, ts.COLUMN_SIZE, 2 * (ts.REGION_SIZE_N ** 2 * ts.COLUMN_SIZE))]
    for _ in range(5):
        merged_move(r)
