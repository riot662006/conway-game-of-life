import pygame
import sys

from entities.board import Board

import entities.common_patterns as patterns
from entities.patterns import Pattern


def board_setup(screen):
    board = Board(screen, (0, 0), (50, 50), 10, wrap=False)  # board. refer to entities/board

    board.add_pattern(Pattern.open('lwss.rle').flip_y(), (0, 10))
    board.add_pattern(Pattern.open('lwss.rle'), (42, 10))

    print(board.export(strip=True))
    board.set_cell((9, 9), True)

    return board


def run_game():
    # technically a simulation but its called the Conway's 'GAME' of life. =)
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

    board = board_setup(screen)

    elapsed_time = 0  # to calc time since last board update
    running = True
    while running:
        for event in pygame.event.get():  # pygame pending events list
            if event.type == pygame.QUIT:  # if one of those events is pressing the 'X' button
                running = False  # end run

        clock.tick(fps)  # like time.sleep but pygame prefers this

        # for next board frame
        elapsed_time += 1000 / fps

        if elapsed_time >= delay_time:
            screen.fill((0, 0, 0))  # clear screen for next frame
            elapsed_time = 0
            board.next_position()
            board.draw_board()
            pygame.display.flip()  # actually updates pixels

    # closes the window and allows the program to end
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    run_game()
