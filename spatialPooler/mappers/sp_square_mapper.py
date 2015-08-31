
class SquareMapper:
    @staticmethod
    def map_оne(input_wh, colcoord, radius):
        # адаптер
        pass

    @staticmethod
    def map_all(self, input_wh, cols_wh, radius):
        # адаптер
        pass

    @staticmethod
    def get_mapped_columns(input_size, output_size, radius):
        # получает все маппинги, отдает в виде списка пар
        result = []

        for i in range(output_size):
            for j in range(output_size):
                result.append(SquareMapper.get_columns_cells_by_coord(i, j, input_size, output_size, radius))

        return result

    @staticmethod
    def get_columns_cells_by_coord(x, y, input_size, output_size, radius):
        # метод получает все поля которые принадлежат квадрату заданного радиуса с центром в x, y
        assert (input_size > 0)
        assert (output_size > 0)
        assert (input_size >= output_size)
        assert (0 <= x < output_size)
        assert (0 <= y < output_size)

        result = []

        offset = 1.0 * input_size / output_size / 2.0
        rx = offset + x * 2.0 * offset
        ry = offset + y * 2.0 * offset

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
