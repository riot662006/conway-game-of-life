class PatternRLE:
    class StillLife:
        block = "2o$2o!"
        beehive = "b2o$o2bo$b2o!"
        loaf = "b2ob$o2bo$bobo$2bo!"
        boat = "2o$obo$bo!"
        tub = "bo$obo$bo!"

    class Oscillator:
        beacon = "2o$2o$2b2o$2b2o!"

    class SpaceShip:
        glider = "2bo$obo$b2o!"
        lwss = "o2bo$4bo$o3bo$b4o!"
        copperhead = "b2o2b2o$3b2o$3b2o$obo2bobo$o6bo2$o6bo$b2o2b2o$2b4o2$3b2o$3b2o!"

    class Gun:
        gosper = "24bo$22bobo$12b2o6b2o12b2o$11bo3bo4b2o12b2o$" \
                 "2o8bo5bo3b2o$2o8bo3bob2o4bobo$10bo5bo7bo$11bo3bo$12b2o!"
        simkin = "2o5b2o$2o5b2o2$4b2o$4b2o5$22b2ob2o$21bo5bo$" \
                 "21bo6bo2b2o$21b3o3bo3b2o$26bo4!"


    @staticmethod
    def pat(p):
        assert not (any([a not in "bo$!1234567890" for a in p])), "Invalid character for RLE format"
        assert p.find('!') == -1 or p.find('!') == len(p) - 1, "'!' must be at the end of the pattern"

        p = p if p[-1] != '!' else p[:-1]
        pattern = []

        j = 0

        for line in p.split("$"):
            i = 0
            num = ''
            for c in line:
                if c in "1234567890":
                    num += c
                else:
                    num = int(num) if len(num) else 1
                    if c == 'o':
                        pattern += [(i, j) for i in range(i, i + num)]
                    i += num
                    num = ''

            j += int(num) if len(num) else 1

        return pattern

    @staticmethod
    def rle(pattern: list[tuple]):
        # sorts the pattern by the y-axis then the x-axis
        pattern.sort(key=lambda x: (x[1], x[0]))
        lines = []
        p = ""
        compressed_p = ""

        # to split the pattern into lines using the y-axis as the seperator
        for x in pattern:
            if len(lines) == 0:
                lines.append([x])
            else:
                if lines[-1][-1][1] == x[1]:
                    lines[-1].append(x)
                else:
                    lines.append([x])

        # to get all the character for dead and alive cells, end of a line and end of the pattern
        while len(lines):
            line = lines.pop(0)
            prev = -1
            for point in line:
                if point[0] - prev - 1 != 0:
                    p += "b" * (point[0] - prev - 1)
                p += "o"
                prev = point[0]

            p += '$' * (lines[0][0][1] - line[0][1]) if len(lines) else '!'

        # to compress this data to RLE format. two-pointer method for now.
        start = 0
        end = 1

        while p[start] != '!':
            if p[end] == '!' or p[end] != p[start]:
                compressed_p += (str(end - start) if end - start > 1 else "") + p[start]
                start = end

            end += 1

        return compressed_p + "!"


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


guns = [
    "24bo$22bobo$12b2o6b2o12b2o$11bo3bo4b2o12b2o$"
    "2o8bo5bo3b2o$2o8bo3bob2o4bobo$10bo5bo7bo$11bo3bo$12b2o!",
]

if __name__ == '__main__':
    pat = still_life['tub']
    print(PatternRLE.rle([(2, 0), (0, 1), (2, 1), (1, 2), (2, 2)]),
        PatternRLE.rle([(0, 0), (3, 0), (4, 1), (0, 2), (4, 2), (1, 3), (2, 3), (3, 3), (4, 3)]))
