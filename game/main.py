import pygame
import sys

from entities.board import Board

import entities.patterns as patterns
from entities.patterns import PatternRLE


def run_game():
    pygame.init()

    # Some display variables
    screen_width = 1000
    screen_height = 600
    fps = 60
    delay_time = 30

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Conway's Game of Life")

    clock = pygame.time.Clock()

    board = Board(screen, (0, 0), (100, 100), 5, wrap=True)

    board.revive_cells(PatternRLE.pat(PatternRLE.Oscillator.beacon), (5, 5))
    board.revive_cells(PatternRLE.pat(PatternRLE.Gun.simkin), (40, 40))
    board.update()

    elapsed_time = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        board.draw_board()
        pygame.display.flip()

        clock.tick(fps)

        elapsed_time += 1000 / fps

        if elapsed_time >= delay_time:
            elapsed_time = 0
            board.next_position()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    run_game()
