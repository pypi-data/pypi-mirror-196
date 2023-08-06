import numpy as np


class SudokuCore:
    def __init__(self):
        """
        :param
        """
        self.total_size = None  # size of sudoku = total_size * total_size, can be 4,9,16...
        self.grid = None
        self.cell_size = None
        self.possible_numbers = None

    def __str__(self):
        return str(self.grid)

    def init(self, size):
        """
        Init sudoku object based on size parameter
        :param size: int, defines size of sudoku grid, i.e. 4 for numbers 1-4, 9 for numbers 1-9 etc.
        :return:
        """
        self.total_size = size  # size of sudoku = total_size * total_size, can be 4,9,16...
        self.grid = np.zeros((self.total_size, ) * 2, dtype=int)
        self.cell_size = int(self.total_size ** 0.5)
        self.init_possible_numbers()

    def from_grid(self, grid):
        """
        Alternative initialization, which uses supplied sudoku grid.
        :param grid:
        :return:
        """
        self.grid = np.asarray(grid)
        self.total_size = len(grid[0])
        self.cell_size = int(self.total_size ** 0.5)
        self.reset_possible_numbers()

    def init_possible_numbers(self):
        self.possible_numbers = np.ndarray((self.total_size, ) * 3, dtype=bool)
        self.possible_numbers.fill(True)

    def get_next_free_position(self):
        """
        Return next grid position with no number assigned.
        :return:
        """
        for position in np.ndindex(self.grid.shape):
            if self.grid[position] == 0:
                return position
        return -1

    def any_free_position(self):
        return np.any(self.grid == 0)

    def get_empty_positions(self):
        return self.grid == 0

    def get_size(self):
        return self.total_size

    def get_position(self, position):
        """
        Get value of position in sudoku grid.
        :param position:
        :return:
        """
        return self.grid[position]

    def clean_position(self, position):
        self.grid[position] = 0
        self.reset_possible_numbers()

    def fill_position(self, position, value):
        self.grid[position] = value
        self.update_options_single_number(position, value)

    def reset_possible_numbers(self):
        """
        Re-generate possible numbers based on grid contents
        :return:
        """
        self.init_possible_numbers()
        for position in np.ndindex(self.grid.shape):
            if self.grid[position] != 0:
                self.update_options_single_number(position, self.grid[position])

    def update_options_single_number(self, position, number):
        """
        Update possible numbers for positions based on sudoku rules.
        :param position: tuple(x, y)
        :param number: int
        :return:
        """
        self.update_row(position[0], number)
        self.update_column(position[1], number)
        self.update_cell(position, number)

    def update_row(self, row, number):
        """
        Update possible numbers based on sudoku rule which allows only one number of a kind in a row.
        :param row:
        :param number:
        :return:
        """
        self.possible_numbers[row, :, number-1] = False

    def update_column(self, column, number):
        """
        Update possible numbers based on sudoku rule which allows only one number of a kind in a column.
        :param column:
        :param number:
        :return:
        """
        self.possible_numbers[:, column, number-1] = False

    def update_cell(self, position, number):
        """
        Update possible numbers based on sudoku rule which allows only one number of a kind in a cell.
        :param position:
        :param number:
        :return:
        """
        cell_x = (position[0] // self.cell_size) * self.cell_size
        cell_y = (position[1] // self.cell_size) * self.cell_size
        self.possible_numbers[cell_x:cell_x + self.cell_size, cell_y:cell_y + self.cell_size, number-1] = False

    def check_next_single_option_position(self):
        """
        Scan grid for next position, which has only 1 number possible as option.
        :return: coords (x, y) or -1 if not found
        """
        for position in np.ndindex(self.possible_numbers.shape[:2]):
            if sum(self.possible_numbers[position]) == 1 and self.get_position(position) == 0:
                return position
        return -1

    def check_solvable(self):
        """
        Attempt to solve sudoku. Returns True if it is possible to solve it based on implemented solving steps.
        :return:
        """
        original_grid = self.grid.copy()
        solvable = self.solve()
        self.grid = original_grid
        self.reset_possible_numbers()
        return solvable

    def solve(self):
        self.reset_possible_numbers()
        while True:
            if (position := self.check_next_single_option_position()) != -1:
                single_option_value = np.where(self.possible_numbers[position])[0] + 1
                self.fill_position(position, single_option_value)
            elif self.check_next_single_option_position() == -1:
                return not (self.grid == 0).any()
