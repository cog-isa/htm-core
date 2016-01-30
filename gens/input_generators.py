from random import randrange, shuffle


class MakeBubble:
    def __init__(self, inner_generator, square_size, scale):
        self.inner_generator = inner_generator(square_size)
        self.scale = scale
        self.square_size = square_size

    def move(self):
        self.inner_generator.move()

    def out(self):
        a = self.get_data()
        for i in a:
            print(i)
        print()

    def get_data(self):
        result = [[0 for _ in range(self.square_size * self.scale)] for _ in range(self.square_size * self.scale)]
        a = self.inner_generator.get_data()
        for i in range(self.square_size):
            for j in range(self.square_size):
                if a[i][j]:
                    for x in range(i * self.scale, (i + 1) * self.scale):
                        for y in range(j * self.scale, (j + 1) * self.scale):
                            result[x][y] = 1
        return result


class TestSimpleSteps:
    def __init__(self, square_size):
        self.square_size = square_size
        self.a = [[0 for _ in range(square_size)] for _ in range(square_size)]
        self.current_step = 0
        self.state = "MOVE_FORWARD"
        self.a[self.current_step][self.current_step] = 1

    def move(self):
        self.a[self.current_step][self.current_step] = 0
        if self.state == "MOVE_FORWARD":
            if self.current_step == self.square_size - 1:
                self.state = "MOVE_BACKWARD"
        else:
            if self.current_step == 0:
                self.state = "MOVE_FORWARD"

        if self.state == "MOVE_FORWARD":
            self.current_step += 1
        else:
            self.current_step -= 1

        self.a[self.current_step][self.current_step] = 1

    def out(self):
        for i in self.a:
            print(i)
        print()

    def get_data(self):
        return self.a


class TooTestSimpleSteps:
    def __init__(self, square_size):
        self.square_size = square_size
        self.a = [[0 for _ in range(square_size)] for _ in range(square_size)]
        self.current_step = 0
        self.state = "MOVE_FORWARD"
        self.a[self.current_step][self.current_step] = 1

    def move(self):
        self.a[0][self.current_step] = 0
        if self.state == "MOVE_FORWARD":
            if self.current_step == self.square_size - 1:
                self.state = "MOVE_BACKWARD"
        else:
            if self.current_step == 0:
                self.state = "MOVE_FORWARD"

        if self.state == "MOVE_FORWARD":
            self.current_step += 1
        else:
            self.current_step -= 1

        self.a[0][self.current_step] = 1

    def out(self):
        for i in self.a:
            print(i)
        print()

    def get_data(self):
        return self.a


class Too2TestSimpleSteps:
    def __init__(self, square_size):
        self.square_size = square_size
        self.a = [[0 for _ in range(square_size)] for _ in range(square_size)]
        self.current_step = 0
        self.state = "MOVE_FORWARD"
        self.a[self.current_step][self.current_step] = 1
        self.a[self.current_step][self.current_step + 1] = 1

    def move(self):
        self.a[self.current_step][self.current_step] = 0
        self.a[self.current_step][self.current_step + 1] = 0
        if self.state == "MOVE_FORWARD":
            if self.current_step == self.square_size - 2:
                self.state = "MOVE_BACKWARD"
        else:
            if self.current_step == 0:
                self.state = "MOVE_FORWARD"

        if self.state == "MOVE_FORWARD":
            self.current_step += 1
        else:
            self.current_step -= 1

        self.a[self.current_step][self.current_step] = 1
        self.a[self.current_step][self.current_step + 1] = 1

    def out(self):
        for i in self.a:
            print(i)
        print()

    def get_data(self):
        return self.a


class HardSteps:
    def __init__(self, square_size):
        self.square_size = square_size
        self.a = [[0 for _ in range(square_size)] for _ in range(square_size)]
        self.current_step = 0
        self.state = "MOVE_FORWARD"
        self.a[self.current_step][self.current_step] = 1

        self.moves = []
        self.moves.append([0, 0])
        self.moves.append([1, 1])
        self.moves.append([2, 2])
        self.moves.append([1, 1])
        self.moves.append([0, 0])
        self.moves.append([0, 1])
        self.moves.append([0, 2])
        self.moves.append([1, 1])
        self.moves.append([2, 0])
        self.moves.append([1, 1])
        self.moves.append([0, 2])
        self.moves.append([0, 1])
        self.size = len(self.moves)

    def move(self):
        x, y = self.moves[self.current_step]
        self.a[x][y] = 0
        self.current_step = (self.current_step + 1) % self.size
        x, y = self.moves[self.current_step]
        self.a[x][y] = 1

    def out(self):
        for i in self.a:
            print(i)
        print()

    def get_data(self):
        return self.a


class HardStepsLen2:
    def __init__(self, square_size):
        self.square_size = square_size
        self.a = [[0 for _ in range(square_size)] for _ in range(square_size)]
        self.current_step = 0
        self.state = "MOVE_FORWARD"
        self.a[self.current_step][self.current_step] = 1

        self.moves = []
        self.moves.append([0, 0])
        self.moves.append([2, 2])
        self.moves.append([4, 4])
        self.moves.append([2, 2])
        self.moves.append([0, 0])
        self.moves.append([0, 1])
        self.moves.append([0, 2])
        self.moves.append([0, 3])
        self.moves.append([0, 4])
        self.moves.append([2, 2])
        self.moves.append([4, 0])
        self.moves.append([2, 2])
        self.moves.append([0, 4])
        self.moves.append([0, 3])
        self.moves.append([0, 2])
        self.moves.append([0, 1])
        print("moves: ", len(self.moves))
        # self.moves.append([0,0])
        self.size = len(self.moves)

    def move(self):
        x, y = self.moves[self.current_step]
        self.a[x][y] = 0
        self.current_step = (self.current_step + 1) % self.size
        x, y = self.moves[self.current_step]
        self.a[x][y] = 1

    def out(self):
        for i in self.a:
            print(i)
        print()

    def get_data(self):
        return self.a


class Cross:
    def __init__(self, square_size):
        self.square_size = square_size
        self.a = [[0 for _ in range(square_size)] for _ in range(square_size)]
        self.center_x = self.x = (square_size - 1) // 2
        self.center_y = self.y = (square_size - 1) // 2
        self.kx = [1, -1, 0, 0]
        self.ky = [0, 0, -1, 1]
        self.state = 0
        self.direction = 1
        self.a[self.x][self.y] = 1

    def ok(self, x, y):
        return 0 <= x < self.square_size and 0 <= y < self.square_size

    def move(self):
        self.a[self.x][self.y] = 0
        if self.x == self.center_x and self.y == self.center_y:
            self.state = (self.state + 1) % len(self.kx)
            self.direction = 1

        if self.direction:
            new_x = self.x + self.kx[self.state]
            new_y = self.y + self.ky[self.state]
        else:
            new_x = self.x - self.kx[self.state]
            new_y = self.y - self.ky[self.state]

        if self.ok(new_x, new_y):
            self.x = new_x
            self.y = new_y
            self.a[self.x][self.y] = 1
        else:
            self.direction = 0
            self.a[self.x][self.y] = 1
            self.move()

    def out(self):
        for i in self.a:
            print(i)
        print()

    def get_data(self):
        return self.a


class ConstantActiveBit:
    def __init__(self, square_size):
        self.square_size = square_size
        assert (square_size >= 2)
        self.a = [[0 for _ in range(square_size)] for _ in range(square_size)]
        self.a[0][0] = 1
        self.x = 0
        self.y = 1
        self.state = 0
        self.MOD = 6

    def move(self):
        if self.state > 2:
            self.a[self.x][self.y] = 1
        else:
            self.a[self.x][self.y] = 0
        self.state = (self.state + 1) % self.MOD

    def out(self):
        for i in self.a:
            print(i)
        print()

    def get_data(self):
        return self.a


class Snake:
    def __init__(self, square_size):
        self.SNAKE = 1
        self.FOOD = 2
        self.EMPTY = 0

        self.step_number = -5

        self.square_size = square_size
        self.a = [[0 for _ in range(square_size)] for _ in range(square_size)]
        self.kx = [1, 0, -1, 0]
        self.ky = [0, 1, 0, -1]
        self.direction = 0
        self.snake_size = 4

        self.new_food_x, self.new_food_y = -1, -1

        self.snake_tail = [[self.square_size // 2, self.square_size // 2] for _ in range(self.snake_size)]
        print(self.snake_tail)
        for i in self.snake_tail:
            print(i[0], i[1])
            self.a[i[0]][i[1]] = self.SNAKE

        self.game_over = False

    @staticmethod
    def square_dist(x1, y1, x2, y2):
        return (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)

    def out(self):
        for i in self.a:
            print(i)

    def ok(self, x, y):
        return 0 <= x < self.square_size and 0 <= y < self.square_size and self.a[x][y] != self.SNAKE

    def move(self):
        self.step_number += 1
        directions = [-1, 1, 0]
        shuffle(directions)

        ok_tx, ok_ty = -1, -1
        ok_direction = self.direction

        # ищем любой ок переход
        for i in directions:
            new_direction = (self.direction + i + 4) % 4
            tx, ty = self.snake_tail[0][0] + self.kx[new_direction], self.snake_tail[0][1] + self.ky[new_direction]

            if self.ok(tx, ty):
                ok_tx, ok_ty = tx, ty
                ok_direction = new_direction
                break

        # если есть пища, то ищем выгодный переход
        if self.ok(self.new_food_x, self.new_food_y) and self.a[self.new_food_x][self.new_food_y] == self.FOOD:
            for i in directions:
                new_direction = (self.direction + i + 4) % 4
                tx, ty = self.snake_tail[0][0] + self.kx[new_direction], self.snake_tail[0][1] + self.ky[new_direction]
                if self.ok(tx, ty) and self.square_dist(tx, ty, self.new_food_x, self.new_food_y) < self.square_dist(
                        self.snake_tail[0][0], self.snake_tail[0][1], self.new_food_x, self.new_food_y):
                    ok_tx, ok_ty = tx, ty
                    ok_direction = new_direction
                    break

        if self.ok(ok_tx, ok_ty):
            self.direction = ok_direction
            print(self.snake_tail)
            if self.a[ok_tx][ok_ty] == self.FOOD:
                last_index = len(self.snake_tail) - 1
                self.snake_tail.append([self.snake_tail[last_index][0], self.snake_tail[last_index][1]])

            for j in self.snake_tail:
                self.a[j[0]][j[1]] = self.EMPTY

            for q in range(1, len(self.snake_tail)):
                j = len(self.snake_tail) - q
                self.snake_tail[j] = [self.snake_tail[j - 1][0], self.snake_tail[j - 1][1]]
            self.snake_tail[0] = [ok_tx, ok_ty]

            for j in self.snake_tail:
                self.a[j[0]][j[1]] = self.SNAKE

            if self.step_number % 10 == 0:
                if self.ok(self.new_food_x, self.new_food_y) and self.a[self.new_food_x][self.new_food_y] == self.FOOD:
                    self.a[self.new_food_x][self.new_food_y] = self.EMPTY

                self.new_food_x, self.new_food_y = randrange(0, self.square_size), randrange(0, self.square_size)

                if self.a[self.new_food_x][self.new_food_y] == self.EMPTY:
                    self.a[self.new_food_x][self.new_food_y] = self.FOOD

        else:
            self.game_over = True
            print("GAME_END")

    def get_data(self):
        res = [[0 for _ in range(self.square_size)] for _ in range(self.square_size)]
        for i in range(self.square_size):
            for j in range(self.square_size):
                res[i][j] = self.a[i][j]
                if res[i][j] == self.FOOD:
                    res[i][j] = 1
        return res


class Hierarchy2l:
    def __init__(self, square_size):
        assert (square_size == 4)

        self.square_size = square_size

        self.a = [0, 0]
        self.b = [0, 3]
        self.cur = 0
        self.go = ['a', 'b', 'a', 'b', 'b', 'a']

    def move(self):

        if self.go[self.cur] == 'a':
            x, y = self.a
            if x == 3 and y == 3:
                self.a = [0, 0]
                self.cur = (self.cur + 1) % len(self.go)
            else:
                self.a = [x + 1, y + 1]
        else:
            x, y = self.b
            if x == 3 and y == 0:
                self.b = [0, 3]
                self.cur = (self.cur + 1) % len(self.go)
            else:
                self.b = [x + 1, y - 1]

    def out(self):
        for i in self.get_data():
            print(i)
        print()

    def get_data(self):
        result = [[0 for _ in range(self.square_size)] for _ in range(self.square_size)]
        if self.go[self.cur] == 'a':
            x, y = self.a
        else:
            x, y = self.b
        result[x][y] = 1
        return result


class SequenceLoader:
    # засовываем в этот генератор уже готовую последовательность, он выдает ее по шагам - профит
    def __init__(self, square_size, a):
        self.a = a
        self.square_size = square_size
        self.cnt = 0

    def move(self):
        self.cnt += 1

    def out(self):
        for i in self.get_data():
            print(i)
        print()

    def get_data(self):
        return self.a[self.cnt]


if __name__ == "__main__":
    s = Snake(5)
