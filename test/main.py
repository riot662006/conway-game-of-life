from game.main import *

if __name__ == '__main__':
    # Some display variables
    screen_width = 1000
    screen_height = 600

    pygame.init()
    S = pygame.display.set_mode((screen_width, screen_height))

    l_lwss = Pattern.open('lwss.rle')
    r_lwss = l_lwss.flip_y()

    pat = Pattern()
    g = GameOfLife(S, board_size=(98, 90), pixel_size=6, update_at_start=False, board_wrap=True)

    for i in range(0, 98, 7):
        for j in range(0, 96, 12):
            pat = pat.add((l_lwss if j % 24 else r_lwss), (i, j))

    pat = pat.clear((20, 20, 20, 20))
    pat = pat.clear((61, 60, 21, 21))

    g.board.add_pattern(pat)
    g.mainloop()
