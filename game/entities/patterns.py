still_life = {
    'block': [(0, 0), (1, 0), (0, 1), (1, 1)],
    'beehive': [(1, 0), (2, 0), (0, 1), (3, 1), (1, 2), (2, 2)],
    'loaf': [(1, 0), (2, 0), (0, 1), (3, 1), (1, 2), (3, 2), (2, 3)],
    'boat': [(0, 0), (1, 0), (0, 1), (2, 1), (1, 2)],
    'tub': [(1, 0), (0, 1), (2, 1), (1, 2)]
}

spaceship = {
    'glider': [(2, 0), (0, 1), (2, 1), (1, 2), (2, 2)],
    'lwss': [(0, 0), (3, 0), (4, 1), (0, 2), (4, 2), (1, 3), (2, 3), (3, 3), (4, 3)]
}

oscillator = {
    'blinker': [(0, 0), (1, 0), (2, 0)],
    'toad': [(1, 0), (2, 0), (3, 0), (0, 1), (1, 2), (2, 2)]
}

tests = [
    [
        (0, 0), (1, 0), (2, 0), (4, 0),
        (0, 1),
        (3, 2), (4, 2),
        (1, 3), (2, 3), (4, 3),
        (0, 4), (2, 4), (4, 4)
    ]
]


def rle(p: str):
    assert not (any([a not in "bo$!1234567890" for a in p])), "Invalid character for RLE format"
    assert p.find('!') == -1 or p.find('!') == len(p) - 1, "'!' must be at the end of the pattern"

    p = p if p[-1] != '!' else p[:-1]
    pattern = []

    j = 0
    for line in p.split("$"):
        num = ''
        i = 0
        for c in line:
            if c in "1234567890":
                num += c
            else:
                num = int(num) if len(num) else 1
                if c == 'o':
                    pattern += [(i, j) for i in range(i, i + num)]
                i += num
                num = ''

        j += 1

    return pattern


guns = [
    "24bo$22bobo$12b2o6b2o12b2o$11bo3bo4b2o12b2o$"
    "2o8bo5bo3b2o$2o8bo3bob2o4bobo$10bo5bo7bo$11bo3bo$12b2o!",

]
