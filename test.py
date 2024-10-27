import unittest
from main import Grid
from main import Direction

class TestGridMerge(unittest.TestCase):
    def test_eq(self):
        ex = Grid.WithPos((0,0))
        grid = Grid.WithPos((0,0))

        self.assertEqual(ex, grid)

    def test_merge_up_no_merge(self):
        ex = Grid.WithPos((0,1), (0,3))
        
        grid = Grid.WithPos((0,1),(1,3))
        grid.move(Direction.UP)
        self.assertEqual(ex, grid)

    def test_0_2_0_2(self):
        ex = Grid.WithPos((0, 0, 4))

        grid = Grid.WithPos((1, 0, 2), (3, 0, 2))
        grid.move(Direction.UP)
        self.assertEqual(ex, grid)

    def test_2_0_0_2(self):
        ex = Grid.WithPos((0, 0, 4))

        grid = Grid.WithPos((0, 0, 2), (3, 0, 2))
        grid.move(Direction.UP)
        self.assertEqual(ex, grid)

    def test_2_4_2_0(self):
        ex = Grid.WithPos((0, 0, 2), (1, 0, 4), (2, 0, 2))

        grid = Grid.WithPos((0, 0, 2), (1, 0, 4), (2, 0, 2))
        grid.move(Direction.UP)
        self.assertEqual(ex, grid)

    def test_0_2_4_2(self):
        ex = Grid.WithPos((0, 0, 2), (1, 0, 4), (2, 0, 2))

        grid = Grid.WithPos((1, 0, 2), (2, 0, 4), (3, 0, 2))
        grid.move(Direction.UP)
        self.assertEqual(ex, grid)

    def test_2_4_0_2(self):
        ex = Grid.WithPos((0, 0, 2), (1, 0, 4), (2, 0, 2))

        grid = Grid.WithPos((0, 0, 2), (1, 0, 4), (3, 0, 2))
        grid.move(Direction.UP)
        self.assertEqual(ex, grid)

    def test_0_2_0_4(self):
        ex = Grid.WithPos((0, 0, 2), (1, 0, 4))

        grid = Grid.WithPos((1, 0, 2), (3, 0, 4))
        grid.move(Direction.UP)
        self.assertEqual(ex, grid)

    def test_rotate(self):
        """
        0 0 0 0 -> 0 0 0 0
        0 2 0 0    4 0 2 0
        0 0 0 8    0 0 0 0
        0 4 0 0    0 8 0 0
        """
        ex = Grid.WithPos((1, 0, 4), (1, 2, 2), (3, 1, 8))

        grid = Grid.WithPos((1, 1, 2), (2, 3, 8), (3, 1, 4))
        grid._rotate_cw()
        self.assertEqual(ex, grid)

    def test_2_0_0_0(self):
        grid = Grid.WithPos((0,0,2))
        moved = grid.move(Direction.UP)
        self.assertFalse(moved)

    def test_2_2_2_2(self):
        ex = Grid.WithPos((0, 0, 4), (1, 0, 4))

        grid = Grid.WithPos((0, 0, 2), (1, 0, 2), (2, 0, 2), (3, 0, 2))
        grid.move(Direction.UP)
        self.assertEqual(ex, grid)

if __name__ == "__main__":
    unittest.main()
