import pygame
from enum import Enum

from .pattern.patterns import Pattern, PatternFinite


class GameState(Enum):
    NORMAL_SPEED_FORWARD = 0
    PAUSED = 1


class GameOfLife:
    def __init__(self, screen: pygame.Surface | pygame.SurfaceType, /
                 , board_pos=(0, 0), board_size=(100, 100), board_wrap=True, pixel_size=5,
                 fps=60, sim_frame_time=30, update_at_start=True):
        self.screen = screen
        self.fps = fps
        self.sim_frame_time = sim_frame_time

        self.board = PatternFinite(board_size)

        self.board_pos = board_pos
        self.board_size = board_size
        self.pixel_size = pixel_size
        self.board_wrap = board_wrap

        self.sim_clock = pygame.time.Clock()

        self._state: GameState = GameState.NORMAL_SPEED_FORWARD if update_at_start else GameState.PAUSED

    def next_position(self):
        to_check = set()

        for x, y in self.board.alive_cells:
            for xi in range(x - 1, x + 2):
                for yi in range(y - 1, y + 2):
                    if self.board_wrap:
                        to_check.add((xi % self.board_size[0], yi % self.board_size[1]))
                    else:
                        to_check.add((xi, yi))

        to_update = []

        for x, y in to_check:
            alive_neighbors = 0
            for xi in range(x - 1, x + 2):
                for yi in range(y - 1, y + 2):
                    if not(xi == x and yi == y):
                        if self.board_wrap:
                            alive_neighbors += int(self.board.alive((xi % self.board_size[0], yi % self.board_size[1])))
                        else:
                            alive_neighbors += int(self.board.alive((xi, yi)))

            if self.board.alive((x, y)):
                if alive_neighbors > 3 or alive_neighbors < 2:
                    to_update.append((x, y, False))
            else:
                if alive_neighbors == 3:
                    to_update.append((x, y, True))

        del to_check

        for x, y, on in to_update:
            if on:
                self.board.on((x, y))
            else:
                self.board.off((x, y))

    def next_frame(self):
        self.next_position()
        self.draw_board()

    def draw_board(self):
        """
                Draws the board and the alive cells on them.
                """

        # background

        pygame.draw.rect(self.screen, 'grey',
                         (*self.board_pos,
                          self.board_size[0] * self.pixel_size, self.board_size[1] * self.pixel_size))

        for i, j in self.board.alive_cells:
            x, y = self.board_pos[0] + (i * self.pixel_size), self.board_pos[1] + (j * self.pixel_size)

            # alive cell at (x,y)
            pygame.draw.rect(self.screen, 'white',
                             (x, y, self.pixel_size, self.pixel_size))

        pygame.display.flip()

    def mainloop(self):
        # initial state of the board
        next_frame_timer = 0
        self.draw_board()

        # for the pygame window simulation
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:  # to control the state of the game
                    # space toggles paused state and normal play
                    if event.key == pygame.K_SPACE:
                        if self._state != GameState.PAUSED:
                            self._state = GameState.PAUSED
                            next_frame_timer = 0
                        else:
                            self._state = GameState.NORMAL_SPEED_FORWARD

                    # if paused, this allows to move frame by frame forward
                    elif event.key == pygame.K_RIGHT and self._state == GameState.PAUSED:
                        self.next_frame()

            # updated logic for the next frame. incorporates the state in evaluating now.
            if self._state == GameState.NORMAL_SPEED_FORWARD:
                next_frame_timer += 1000/self.fps
                self.sim_clock.tick(self.fps)

                if next_frame_timer >= self.sim_frame_time:
                    next_frame_timer = 0
                    self.next_frame()

        pygame.quit()