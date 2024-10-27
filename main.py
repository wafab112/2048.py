import numpy as np
import random
import re
from enum import Enum

def get_new_number():
    rn = random.randrange(5)
    if rn == 0:
        return 4
    return 2

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Grid:
    def __init__(self):
        self.arr = [[0 for _ in range(4)] for _ in range(4)]

    @staticmethod
    def Rand():
        grid = Grid()
        grid.add_number(2)
        grid.add_number(2)
        return grid

    @staticmethod
    def WithPos(*args):
        """
        Accepts a variable number of 2-(i,j)- or 3-(i,j,value)-tuples.
        If given a 3-tuple the first two numbers give the coordiates and the last number gives the value.
        If given a 2-tuple will be interpreted as the coordiates with value=2.
        *args - all the positions as 3-tuples
        """
        grid = Grid()
        for pos in args:
            if len(pos) == 2:
                grid[pos] = 2
            elif len(pos) == 3:
                grid[(pos[0], pos[1])] = pos[2]
            else:
                raise ValueError("Items of *args must be tuples of length 2 or 3")

        return grid

    def get_empty_indices(self):
        l = []
        for rI, row in enumerate(self.arr):
            for cI, col in enumerate(row):
                if col == 0:
                    l.append((rI, cI))

        return l

    def get_rand_empty_cell(self) -> (int, int):
        l = self.get_empty_indices()
        lLen = len(l)
        rn = random.randrange(lLen)
        return l[rn]

    def add_rand_number(self):
        n = get_new_number()
        self.add_number(n)

    def add_number(self, n):
        cell = self.get_rand_empty_cell()
        self[cell] = n

    def _transpose(self):
        raise NotImplementedError()
        grid = Grid()

        for i in range(4):
            for j in range(4):
                grid[(j,i)] = self[(i,j)]

    def _rotate_cw(self):
        grid = Grid()

        for i in range(4):
            for j in range(4):
                grid[(j, 3 - i)] = self[(i, j)]

        for i in range(4):
            for j in range(4):
                self[(i,j)] = grid[(i,j)]

    def _rotate_cw_n(self, n):
        for _ in range(n):
            self._rotate_cw()

    def move(self, d: Direction) -> bool:
        """
        Moves the grid in the given direction,
        merging in process.

        Returns whether a merge or a movement was executed.
        """
        moved = False

        match d:
            case Direction.UP:
                moved = self._move_up_and_merge()
            case Direction.DOWN:
                self._rotate_cw_n(2)
                moved = self._move_up_and_merge()
                self._rotate_cw_n(2)
            case Direction.LEFT:
                self._rotate_cw_n(1)
                moved = self._move_up_and_merge()
                self._rotate_cw_n(3)
            case Direction.RIGHT:
                self._rotate_cw_n(3)
                moved = self._move_up_and_merge()
                self._rotate_cw_n(1)

        return moved

    # TODO
    # Merge not recursively
    def _move_up_and_merge(self) -> bool:
        """
        Moves the grid up and merges it in the process.
        Returns whether a merge or a movement was executed.
        """
        merged = False
        moved = False

        for i in range(1,4):
            for j in range(4):
                item = self.arr[i][j]
                if item == 0:
                    continue

                for k in reversed(range(0,i)):
                    if self.arr[k][j] == item:
                        self.arr[k][j] *= 2
                        self.arr[k+1][j] = 0
                        merged = True
                        continue
                    elif self.arr[k][j] == 0:
                        self.arr[k][j] = self.arr[k+1][j]
                        self.arr[k+1][j] = 0
                        moved = True
                    else:
                        break

        if merged:
            self._move_up_and_merge()

        return merged or moved

    def __str__(self):
        _str = ""
        for l  in self.arr:
            _str += str(l)
            _str += "\n"

        return _str

    def __getitem__(self, pos):
        i, j = pos
        if 0 <= i < 4 and 0 <= j < 4:
            return self.arr[i][j]

        raise IndexError(str(pos) + " is out of range")

    def __setitem__(self, pos, value):
        i, j = pos
        if 0 <= i < 4 and 0 <= j < 4:
            self.arr[i][j] = value
            return 

        raise IndexError(str(pos) + " is out of range")

    def __eq__(self, other):
        for rI, row in enumerate(self.arr):
            for cI, col in enumerate(row):
                if col != other[(rI, cI)]:
                    return False

        return True


def game_loop(grid):
    try:
        while True:
            direction = input("Give the new direction for merge (WASD), q for quit: ")
            direction = direction.lower()
            direction = re.sub(r"\s+", "", direction, flags=re.UNICODE)

            moved = False

            match direction:
                case "w":
                    moved = grid.move(Direction.UP)
                case "a":
                    moved = grid.move(Direction.LEFT)
                case "s":
                    moved = grid.move(Direction.DOWN)
                case "d":
                    moved = grid.move(Direction.RIGHT)
                case "q":
                    print("Quit game")
                    return
                case _:
                    continue

            if moved:
                grid.add_rand_number()

            print(grid)
    except KeyboardInterrupt:
        print("")
        print("ctrl-c registered")
        print("Quit game")


if __name__ == "__main__":
    g = Grid.Rand()
    print(g)
    game_loop(g)
