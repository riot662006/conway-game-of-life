import pygame
import sys

from entities.board import Board

import entities.common_patterns as patterns
from entities.patterns import Pattern


def board_setup(board):
    board.add_pattern(Pattern.open('gosper.rle'))


def run_game():  # technically a simulation but its called the Conway's 'GAME' of life. =)
    pygame.init()  # initializing pygame

    # Some display variables
    screen_width = 1000
    screen_height = 600
    fps = 60  # shouldn't really need to be changed
    delay_time = 30  # delay time for the board

    # pygame essentials
    screen = pygame.display.set_mode((screen_width, screen_height))  # to display screen
    pygame.display.set_caption("Conway's Game of Life")  # appropriate title

    clock = pygame.time.Clock()  # to control frame rate

    board = Board(screen, (0, 0), (300, 300), 2, wrap=False)  # board. refer to entities/board
    board_setup(board)

    elapsed_time = 0  # to calc time since last board update
    running = True
    while running:
        for event in pygame.event.get():  # pygame pending events list
            if event.type == pygame.QUIT:  # if one of those events is pressing the 'X' button
                running = False  # end run

        screen.fill((0, 0, 0))  # clear screen for next frame
        board.draw_board()
        pygame.display.flip()  # actually updates pixels

        clock.tick(fps)  # like time.sleep but pygame prefers this

        # for next board frame
        elapsed_time += 1000 / fps

        if elapsed_time >= delay_time:
            elapsed_time = 0
            board.next_position()

    # closes the window and allows the program to end
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    run_game()
