# 15-puzzle solver
# template: http://www.codeskulptor.org/#poc_fifteen_template.py
# play online: http://www.codeskulptor.org/#user40_ithWQTHEwM_10.py
"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui


class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]
        if initial_grid is not None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representation for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_row(self, row):
        """
        Returns row
        """
        return self._grid[row]

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def position_tile(self, target, source=None):
        """
        Moves current tile to target tile without screwing anything up
        """
        if source is None:
            source = target
        (target_row, target_col) = target
        (source_row, source_col) = source
        assert target_col > 0
        (idx, idy) = self.current_position(source_row, source_col)
        move = "u" * (target_row - idx)
        if idy > target_col:
            move += "r" * (idy - target_col - 1)
        elif target_col > idy:
            move += "l" * (target_col - idy)
        else:
            move += "ld"
        self.update_puzzle(move)
        while self.current_position(source_row, source_col)[1] < target_col:
            if self.current_position(source_row, source_col)[0] == 0:
                move += "drrul"
                self.update_puzzle("drrul")
            else:
                move += "urrdl"
                self.update_puzzle("urrdl")
        while self.current_position(source_row, source_col)[1] > target_col:
            if self.current_position(source_row, source_col)[0] == 0:
                move += "rdllu"
                self.update_puzzle("rdllu")
            else:
                move += "rulld"
                self.update_puzzle("rulld")
        while self.current_position(source_row, source_col)[0] != target_row:
            move += "druld"
            self.update_puzzle("druld")
        return move

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return row, col
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                # assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][
                    zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                self._grid[zero_row][zero_col] = self._grid[zero_row][
                    zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                # assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][
                    zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][
                    zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        if self._grid[target_row][target_col] != 0:
            return False
        solved = Puzzle(self._height, self._width)
        for row in range(target_row + 1, self._height):
            if self._grid[row] != solved.get_row(row):
                return False
        if self._grid[target_row][target_col + 1:] != \
                solved.get_row(target_row)[target_col + 1:]:
            return False
        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        assert target_row > 1
        assert target_col > 0
        assert self.lower_row_invariant(target_row, target_col)
        move = self.position_tile((target_row, target_col))
        assert self.lower_row_invariant(target_row, target_col - 1)
        return move

    def solve_col0_tile(self, target_row):
        """"
        blah
        """
        move = "ur"
        self.update_puzzle("ur")
        if self.current_position(target_row, 0) != (target_row, 0):
            move += self.position_tile((target_row - 1, 1), (target_row, 0))
            move += "ruldrdlurdluurddlur"
            self.update_puzzle("ruldrdlurdluurddlur")
        move += "r" * (self._width - 2)
        self.update_puzzle("r" * (self._width - 2))
        assert self.lower_row_invariant(target_row - 1,
                                        self._width - 1)
        return move

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        if self.get_number(0, target_col) != 0:
            return False
        solved = Puzzle(self._height, self._width)
        for row in range(2, self._height):
            if self._grid[row] != solved.get_row(row):
                return False
        if self.current_position(1, target_col) != (1, target_col):
            return False
        if self._grid[1][target_col + 1:] != \
                solved.get_row(1)[target_col + 1:]:
            return False
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        return self.lower_row_invariant(1, target_col)

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col)
        move = "ld"
        self.update_puzzle("ld")
        if self.current_position(0, target_col) != (0, target_col):
            move += self.position_tile((1, target_col - 1), (0, target_col))
            move += "urdlurrdluldrruld"
            self.update_puzzle("urdlurrdluldrruld")
        assert self.row1_invariant(target_col - 1)
        return move

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col)
        move = self.position_tile((1, target_col))
        move += "ur"
        self.update_puzzle("ur")
        assert self.row0_invariant(target_col)
        return move

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        assert self.row1_invariant(1)
        move = "lu"
        self.update_puzzle("lu")
        while self.get_number(0, 1) != 1 \
                and self.get_number(1, 0) != self._width:
            move += "rdlu"
            self.update_puzzle("rdlu")
        return move

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        move = ""
        r_count = 0
        d_count = 0
        while True:
            try:
                self.update_puzzle("r")
                r_count += 1
            except IndexError:
                move += r_count * "r"
                break
        while True:
            try:
                self.update_puzzle("d")
                d_count += 1
            except IndexError:
                move += d_count * "d"
                break

        for row in range(2, self._height)[::-1]:
            for col in range(1, self._width)[::-1]:
                assert self.lower_row_invariant(row, col)
                move += self.solve_interior_tile(row, col)
            assert self.lower_row_invariant(row, 0)
            move += self.solve_col0_tile(row)

        for col in range(2, self._width)[::-1]:
            move += self.solve_row1_tile(col)
            self.row0_invariant(col)
            move += self.solve_row0_tile(col)
            self.row1_invariant(col - 1)

        move += self.solve_2x2()

        return move

# Start interactive simulation
poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))
