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
                        for y in range(j * self.scale, (j + 1) *self.scale):
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
