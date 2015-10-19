# from mappers.sp_square_mapper import SquareMapper
from spatialPooler.mappers.sp_square_mapper import SquareMapper


class SquareMapperAutoRadius:
    """
        Адаптер для квадратного маппера,игнорирует заданный радиус и считает его сам автоматически
    """

    @staticmethod
    def map_all(input_wh, cols_wh, radius):
        """
        адаптер для работы SP
        :param input_wh: список из двух элементов размер входа
        :param cols_wh: список из двух элементов размер выхода SP
        :param radius: радиус каждой из колонок (половина стороны квадрата)
        :return: возвращает матрицу список, где для каждой колонки выписаны пары клеток ей принадлежащих
        """
        assert (input_wh[0] == input_wh[1])
        assert (cols_wh[0] == cols_wh[1])
        return SquareMapperAutoRadius.get_mapped_columns(input_wh[0], cols_wh[0], radius)

    @staticmethod
    def get_mapped_columns(input_size, output_size, radius):
        """
        # получает все маппинги для каждой из колонок, для каждой колонки - список пар клеток ей принадлежащих
        :param input_size: размер входа
        :param output_size: размер выхода
        :param radius: радиус каждой из колонок (половина стороны квадрата)
        :return: возвращает матрицу список, где для каждой колонки выписаны пары клеток ей принадлежащих
        """
        print(input_size, output_size)
        offset = 1.0 * input_size / output_size / 2.0
        return SquareMapper.get_mapped_columns(input_size, output_size, offset)

    @staticmethod
    def get_columns_cells_by_coord(x, y, input_size, output_size, radius):
        """
            получает список подключенных к колонке клеток -
        все поля которые принадлежат квадрату заданного радиуса с центром в x, y
        :param x: координата x, колонки
        :param y: координата y, колонки
        :param input_size: размер входа
        :param output_size: размер выхода
        :param radius: радиус не нужен
        :return: список из пар клеток принадлежащих колонке
        """
        offset = 1.0 * input_size / output_size / 2.0
        return SquareMapper.get_columns_cells_by_coord(x, y, input_size, output_size, offset)