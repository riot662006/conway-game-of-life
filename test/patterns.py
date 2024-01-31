from game.entities.patterns import *

if __name__ == '__main__':
    a = Pattern([(1, 0), (0, 1), (4, 0)])
    b = Pattern([(6, 1), (4, 0)])
    c = a.add(b, (0, 3))

    print(a.alive_cells)
    print(b.alive_cells)
    print(c.alive_cells)
