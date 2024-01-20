import pygame
from typing import Optional, List


# a single cell. can't do much. Just be alive or not.
class Cell:
    KILL = 0
    REVIVE = 1


# the board of life. contains the cell grid. also displays the cells
class Board:
    def __init__(self, screen, pos, size, cell_size, /, wrap=False):
        # needed variables.
        self.screen = screen  # where to display it
        self.x, self.y = pos  # position of top-left corner of grid
        self.rows, self.cols = size  # number of rows and columns for grid
        self.cell_size = cell_size  # size of each displayed cell

        self.board: List[List[Optional[Cell]]] = [[None for x in range(self.rows)] for y in range(self.cols)]
        self.updatesLeft = []  # to help delete and revive dead cells

        self.wrapped = wrap  # if the board wraps round. needs to be known when finding neighbors

    # cell getter function
    def __get_cell(self, pos):
        """
        Gets the content of the cell in the position pos. Returns None if pos is out of bounds

        :param pos: tuple[int, int]
        :return: Cell | None
        """
        x, y = pos
        if x < 0 or x >= self.rows or y < 0 or y >= self.cols:
            return None
        else:
            return self.board[y][x]  # made getter function cause this is confusing to remember

    # cell setter function
    def __set_cell(self, pos, obj: Cell | None):
        """
        Sets the cell at position pos to object obj. (Cell if alive and None if dead)

        :param pos: tuple[int, int]
        :param obj: Cell | None
        """
        x, y = pos
        assert 0 <= x < self.rows and 0 <= y < self.cols \
            , f"Invalid position for setting. (x: {x}, y: {y})"
        self.board[y][x] = obj

    def draw_board(self):
        """
        Draws the board and the alive cells on them.
        """

        # background
        pygame.draw.rect(self.screen, 'grey',
                         (self.x, self.y, self.rows * self.cell_size, self.cols * self.cell_size))

        j = 0
        while j < self.cols:
            i = 0
            while i < self.rows:
                if self.__get_cell((i, j)) is not None:  # if is not None then it is a Cell
                    x, y = self.x + (i * self.cell_size), self.y + (j * self.cell_size)

                    # cell x,y
                    pygame.draw.rect(self.screen, 'white',
                                     (x, y, self.cell_size, self.cell_size))
                i += 1
            j += 1

    def revive_cell(self, pos, permissive=True):
        """
        Sets a dead cell to an alive cell.
        :param pos: tuple[int, int]
        :param permissive: boolean
        """

        x, y = pos
        if not permissive:  # if not permissive, makes sure the cell is dead, before reviving it.
            assert self.__get_cell((x, y)) is None, f"Can only revive dead cells. Cell at pos {pos} is alive."
        self.updatesLeft.append((x, y, Cell.REVIVE))  # adds to updates to be made

    def revive_cells(self, pattern, offset=(0, 0)):
        """
        Sets dead cells to alive cells
        :param pattern: list(tuple[int, int])
        :param offset: tuple[int, int]
        """
        for pos in pattern:
            self.revive_cell((pos[0] + offset[0], pos[1] + offset[1]))

    def kill_cell(self, pos, /, permissive=True):
        """
        Sets an alive cell to a dead cell
        :param pos: tuple[int, int]
        :param permissive: boolean
        """

        x, y = pos

        if not permissive:  # like revive cell
            assert self.__get_cell((x, y)) is not None, f"Can only kill at pos {pos} if there is a cell."
        self.updatesLeft.append((x, y, Cell.KILL))  # like revive cell

    def update(self):
        """
        To update the board. Empties updatesLeft variable.
        """

        while len(self.updatesLeft) > 0:
            x, y, action = self.updatesLeft.pop()
            self.__set_cell((x, y), None if action == Cell.KILL else Cell())

    def neighbors(self, pos):
        x, y = pos
        if self.wrapped: # differs when wrapping round
            left, right, up, down = (x - 1) % self.rows, (x + 1) % self.rows, (y - 1) % self.cols, (y + 1) % self.cols

            return [self.__get_cell((left, up)), self.__get_cell((x, up)), self.__get_cell((right, up)),
                    self.__get_cell((left, y)), self.__get_cell((right, y)),
                    self.__get_cell((left, down)), self.__get_cell((x, down)), self.__get_cell((right, down))]

        # When not wrapped, corner and edge positions have None values from the getter function
        return [self.__get_cell((x - 1, y - 1)), self.__get_cell((x, y - 1)), self.__get_cell((x + 1, y - 1)),
                self.__get_cell((x - 1, y)), self.__get_cell((x + 1, y)),
                self.__get_cell((x - 1, y + 1)), self.__get_cell((x, y + 1)), self.__get_cell((x + 1, y + 1))]

    def next_position(self):
        """
            Updates the board to the next generation, following the rules in rules.txt
        """

        j = 0
        while j < self.cols:
            i = 0
            while i < self.rows:
                no_alive_neighbors = sum(1 for x in self.neighbors((i, j)) if x is not None)
                if self.__get_cell((i, j)) is None and no_alive_neighbors == 3:
                    self.revive_cell((i, j))
                elif self.__get_cell((i, j)) is not None and (no_alive_neighbors < 2 or no_alive_neighbors > 3):
                    self.kill_cell((i, j))
                i += 1
            j += 1
        self.update()

