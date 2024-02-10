from game.pattern.patterns import *

if __name__ == '__main__':
    a = PatternFinite((10, 10), [(1, 0), (0, 1), (4, 0), (20, 0)])
    b = a.copy((20, 20))
    b.translate((10, 10))

    c = b.copy()
    c.add(a)

    print(a.alive_cells, a.bbox)
    print(b.alive_cells, b.bbox)
    print(c.alive_cells, c.bbox)

    d = c.translated((5, 10))
    print(d.alive_cells, d.bbox)
