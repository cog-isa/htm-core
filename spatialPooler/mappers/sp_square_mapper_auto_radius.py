from mappers.sp_square_mapper import SquareMapper


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
