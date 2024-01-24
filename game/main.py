import pygame
import sys

from entities.board import Board

import entities.common_patterns as patterns
from entities.patterns import Pattern


class GameOfLife:
    def __init__(self, screen: pygame.Surface | pygame.SurfaceType, /
                 , board_pos=(0, 0), board_size=(100, 100), board_wrap=True, pixel_size=5, fps=60, sim_frame_time=30):
        self.screen = screen
        self.fps = fps
        self.sim_frame_time = sim_frame_time

        self.board = Board(screen, board_pos, board_size, pixel_size, board_wrap)
        self.sim_clock = pygame.time.Clock()

    def next_frame(self):
        self.board.next_position()
        self.board.draw()
        pygame.display.flip()

    def mainloop(self):
        next_frame_timer = 0
        self.board.draw()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            next_frame_timer += 1000/self.fps
            self.sim_clock.tick(self.fps)

            if next_frame_timer >= self.sim_frame_time:
                next_frame_timer = 0
                self.next_frame()
        pygame.quit()


def board_setup(screen):
    board = Board(screen, (0, 0), (50, 50), 10, wrap=False)  # board. refer to entities/board

    board.add_pattern(Pattern.open('lwss.rle').flip_y(), (0, 10))
    board.add_pattern(Pattern.open('lwss.rle'), (42, 10))

    print(board.export(strip=True))
    board.set_cell((9, 9), True)

    return board


if __name__ == '__main__':
    # Some display variables
    screen_width = 1000
    screen_height = 600

    pygame.init()
    S = pygame.display.set_mode((screen_width, screen_height))

    g = GameOfLife(S, board_size=(50, 50), pixel_size=10)

    g.board.add_pattern(Pattern.open('glider.rle'), (0, 0))
    g.board.add_pattern(Pattern.open('glider.rle').flip_y(), (44, 4))

    g.mainloop()
