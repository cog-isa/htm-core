class TestSimpleSteps:
    def __init__(self, square_size):
        self.square_size = square_size
        self.a = [[0 for __ in range(square_size)] for _ in range(square_size)]
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
        self.a = [[0 for __ in range(square_size)] for _ in range(square_size)]
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
        self.a = [[0 for __ in range(square_size)] for _ in range(square_size)]
        self.current_step = 0
        self.state = "MOVE_FORWARD"
        self.a[self.current_step][self.current_step] = 1
        self.a[self.current_step][self.current_step+1] = 1

    def move(self):
        self.a[self.current_step][self.current_step] = 0
        self.a[self.current_step][self.current_step+1] = 0
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
        self.a[self.current_step][self.current_step+1] = 1

    def out(self):
        for i in self.a:
            print(i)
        print()

    def get_data(self):
        return self.a



class HardSteps:
    def __init__(self, square_size):
        self.square_size = square_size
        self.a = [[0 for __ in range(square_size)] for _ in range(square_size)]
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
        self.moves.append([1,1])
        self.moves.append([2,0])
        self.moves.append([1,1])
        self.moves.append([0,2])
        self.moves.append([0,1])
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



class HardStepsLen2:
    def __init__(self, square_size):
        self.square_size = square_size
        self.a = [[0 for __ in range(square_size)] for _ in range(square_size)]
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
        self.moves.append([2,2])
        self.moves.append([4,0])
        self.moves.append([2,2])
        self.moves.append([0,4])
        self.moves.append([0, 3])
        self.moves.append([0,2])
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