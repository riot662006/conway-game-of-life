import pygame
from enum import Enum

from .entities.board import Board
from .entities.patterns import Pattern


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

        self.board = Board(screen, board_pos, board_size, pixel_size, board_wrap)
        self.sim_clock = pygame.time.Clock()

        self._state: GameState = GameState.NORMAL_SPEED_FORWARD if update_at_start else GameState.PAUSED

    def next_frame(self):
        self.board.next_position()
        self.board.draw()
        pygame.display.flip()

    def mainloop(self):
        # initial state of the board
        next_frame_timer = 0
        self.board.draw()
        pygame.display.flip()

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

