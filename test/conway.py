from game.conway import *

if __name__ == '__main__':
    # Some display variables
    screen_width = 1000
    screen_height = 600

    pygame.init()
    S = pygame.display.set_mode((screen_width, screen_height))

    l_lwss = Pattern.open('../pattern/common/lwss.rle')
    r_lwss = l_lwss.copy()
    r_lwss.flip_y()

    g = GameOfLife(S, board_size=(98, 90), pixel_size=6, update_at_start=False, board_wrap=True)

    g.board.add(r_lwss, (2, 2))

    g.mainloop()
