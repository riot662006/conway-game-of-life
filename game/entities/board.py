import pygame
from .patterns import Pattern


# the board of life. contains the cell grid. also displays the cells
class Board:
    def __init__(self, screen, pos, size, cell_size, /, wrap=False):
        # needed variables.
        self.screen = screen  # where to display it
        self.x, self.y = pos  # position of top-left corner of grid
        self.rows, self.cols = size  # number of rows and columns for grid
        self.cell_size = cell_size  # size of each displayed cell

        self.alive_cells = set()  # to keep track of the alive cells

        self.wrapped = wrap  # if the board wraps round. needs to be known when finding neighbors

    # cell getter function
    def is_alive(self, pos):
        """
        Gets the content of the cell in the position pos. Returns false if pos is out of bounds

        :param pos: tuple[int, int]
        :return: bool
        """
        x, y = pos
        if x < 0 or x >= self.rows or y < 0 or y >= self.cols:
            return False
        else:
            return (x, y) in self.alive_cells  # made getter function cause this is confusing to remember

    # cell setter function
    def set_cell(self, pos, state: bool):
        """
        Sets the cell at position pos to alive or dead (true or false).

        :param pos: tuple[int, int]
        :param state: bool
        """
        x, y = pos
        assert 0 <= x < self.rows and 0 <= y < self.cols, f"Invalid position for setting. (x: {x}, y: {y})"

        if not state:
            self.alive_cells.discard((x, y))
        elif state:
            self.alive_cells.add((x, y))

    def draw_board(self):
        """
        Draws the board and the alive cells on them.
        """

        # background
        pygame.draw.rect(self.screen, 'grey',
                         (self.x, self.y, self.rows * self.cell_size, self.cols * self.cell_size))

        for i, j in self.alive_cells:
            x, y = self.x + (i * self.cell_size), self.y + (j * self.cell_size)

            # alive cell at (x,y)
            pygame.draw.rect(self.screen, 'white',
                             (x, y, self.cell_size, self.cell_size))

    def neighbors(self, pos):
        """
            To get the neighbors of the cell at position, pos.
        :param pos: tuple[int, int]
        :return: set[tuple[int, int]]
        """
        x, y = pos
        if self.wrapped:  # differs when wrapping round
            left, right, up, down = (x - 1) % self.rows, (x + 1) % self.rows, (y - 1) % self.cols, (y + 1) % self.cols

            return {(left, up), (x, up), (right, up),
                    (left, y), (right, y),
                    (left, down), (x, down), (right, down)}

        # When not wrapped, corner and edge positions are removed using set operations
        left, right, up, down = (x - 1), (x + 1), (y - 1), (y + 1)
        left_side = {(left, up), (left, y), (left, down)}
        right_side = {(right, up), (right, y), (right, down)}
        top = {(left, up), (x, up), (right, up)}
        bottom = {(left, down), (x, down), (right, down)}

        neighbors = left_side | right_side | top | bottom
        if left == -1:
            neighbors -= left_side
        if right == self.rows:
            neighbors -= right_side
        if up == -1:
            neighbors -= top
        if down == self.cols:
            neighbors -= bottom

        return neighbors

    def alive_neighbors(self, pos):
        """
        Returns the number of alive neighbors that the cell at position pos has.
        :param pos: tuple[int, int]
        :return: int
        """
        num_neighbors = self.neighbors(pos)
        no_alive = 0

        for x in num_neighbors:
            no_alive += int(self.is_alive(x))

        return no_alive

    def next_position(self):
        """
            Updates the board to the next generation, following the rules in rules.txt
        """

        # gets all the alive cells and their neighbors in a set
        # these are the only ones affected by the rules
        # chose this to reduce runtime
        to_update = set()
        for x in self.alive_cells:
            to_update |= self.neighbors(x)
            to_update.add(x)

        # runs through that set and records the cells that are actually going to change
        to_toggle = []

        for x in to_update:
            alive_neighbors = self.alive_neighbors(x)
            # rules applied below. refer to rules.txt. Would add room for change later.
            if self.is_alive(x) and str(alive_neighbors) not in '23':
                to_toggle.append(x)
            elif x not in self.alive_cells and alive_neighbors == 3:
                to_toggle.append(x)

        for x in to_toggle:
            self.set_cell(x, not(self.is_alive(x))) # toggles

    def add_pattern(self, pattern: list[tuple[int, int]] | Pattern, offset=(0, 0)):
        if isinstance(pattern, Pattern):
            pattern = pattern.alive_cells
        if self.wrapped:
            pattern = [((x[0] + offset[0]) % self.rows, (x[1] + offset[1]) % self.cols) for x in pattern]
        else:
            pattern = [(x[0] + offset[0], x[1] + offset[1]) for x in pattern
                       if 0 <= x[0] + offset[0] <= self.rows and 0 <= x[1] + offset[1] <= self.cols]
        self.alive_cells |= set(pattern)
