class SquareMapper:
    """
        Квадратный маппер, назначает каждой колонке точку на входных данных, от этой точки откладывается
    необходимый радиус, все клетки центры которых попадут в этот квадрат - подключаются к колонке
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
        return SquareMapper.get_mapped_columns(input_wh[0], cols_wh[0], radius)

    @staticmethod
    def get_mapped_columns(input_size, output_size, radius):
        """
        # получает все маппинги для каждой из колонок, для каждой колонки - список пар клеток ей принадлежащих
        :param input_size: размер входа
        :param output_size: размер выхода
        :param radius: радиус каждой из колонок (половина стороны квадрата)
        :return: возвращает матрицу список, где для каждой колонки выписаны пары клеток ей принадлежащих
        """

        result = []

        for i in range(output_size):
            for j in range(output_size):
                result.append(SquareMapper.get_columns_cells_by_coord(i, j, input_size, output_size, radius))
        return result

    @staticmethod
    def get_columns_cells_by_coord(x, y, input_size, output_size, radius):
        """
            получает список подключенных к колонке клеток -
        все поля которые принадлежат квадрату заданного радиуса с центром в x, y
        :param x: координата x, колонки
        :param y: координата y, колонки
        :param input_size: размер входа
        :param output_size: размер выхода
        :param radius: радиус колонки (половина стороны квадрата)
        :return: список из пар клеток принадлежащих колонке
        """

        assert (input_size > 0)
        assert (output_size > 0)
        assert (input_size >= output_size)
        assert (0 <= x < output_size)
        assert (0 <= y < output_size)
        assert (radius >= 0)

        result = []

        offset = 1.0 * input_size / output_size / 2.0

        # считаем центр колонки
        rx = offset + x * 2.0 * offset
        ry = offset + y * 2.0 * offset

        # идем по всем клеткам,для каждой клетки и смотрим попадает она или нет
        for i in range(input_size):
            for j in range(input_size):
                if (rx - radius) <= i + 0.5 <= (rx + radius) and (ry - radius) <= j + 0.5 <= (ry + radius):
                    result.append((i, j))

        return result

    @staticmethod
    def out_matrix(x, y, input_size, output_size, radius):
        # отладочный метод - выводит участок, который смаппился на определенные координаты
        a = [[0 for _ in range(input_size)] for _ in range(input_size)]
        s = SquareMapper()
        t = s.get_columns_cells_by_coord(x, y, input_size, output_size, radius)
        print("", t)
        for i in t:
            tx, ty = i
            a[tx][ty] = 1
        for i in a:
            print(i)


if __name__ == "__main__":
    # потестим

    SquareMapper.out_matrix(input_size=10, x=1, y=1, output_size=3, radius=1.51)
    print(SquareMapper.map_all([6, 6], [5, 5], 2))
