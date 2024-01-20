import setuptools
from importlib import resources as impresources
from . import common_patterns


class PatternRLE:  # run length encoding of common_patterns
    # some common common_patterns in classes
    class StillLife:
        block = "2o$2o!"
        beehive = "b2o$o2bo$b2o!"
        loaf = "b2ob$o2bo$bobo$2bo!"
        boat = "2o$obo$bo!"
        tub = "bo$obo$bo!"

    class Oscillator:
        beacon = "2o$2o$2b2o$2b2o!"
        toad = "b3o$o$b2o!"

    class SpaceShip:
        glider = "2bo$obo$b2o!"
        lwss = "o2bo$4bo$o3bo$b4o!"
        copperhead = "b2o2b2o$3b2o$3b2o$obo2bobo$o6bo2$o6bo$b2o2b2o$2b4o2$3b2o$3b2o!"
        fireship = "4bo2bo$4bo2bo$3bo4bo$3bo4bo$3bo4bo$3bo4bo$2b3o2b3o$2bob4obo$" \
                   "3bo4bo3$5b2o$5b2o$5b2o$3bo4bo$b3o4b3o$3o6b3o$2o8b2o$b10o$2b8o$4b4o!"

    class Gun:
        gosper = "24bo$22bobo$12b2o6b2o12b2o$11bo3bo4b2o12b2o$" \
                 "2o8bo5bo3b2o$2o8bo3bob2o4bobo$10bo5bo7bo$11bo3bo$12b2o!"
        simkin = "2o5b2o$2o5b2o2$4b2o$4b2o5$22b2ob2o$21bo5bo$" \
                 "21bo6bo2b2o$21b3o3bo3b2o$26bo4!"

    @staticmethod
    def pat(p):
        """
            Converts an RLE pattern to a pattern for the board.

        :param p: string
        :return: list[tuple[int, int]]
        """
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
        """
            Converts a pattern for the board to an RLE format

        :param pattern: list[tuple[int, int]]
        :return: string
        """
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

    @staticmethod
    def file_to_pat(file, encoding='rle'):
        inp_file = (impresources.files(common_patterns) / file)

        with inp_file.open("rt") as f:
            pat = ""

            for x in f:
                if x[0] not in '#x':
                    pat += x.strip()

            return PatternRLE.pat(pat)

    @staticmethod
    def bounding_box(pattern: list[tuple[int, int]]):
        """
        Finds the size of the bounding box of a pattern.

        :param pattern: list[tuple[int, int]]
        :return: tuple([int, int])
        """

        (left_bound, lower_bound), (right_bound, upper_bound) = pattern[0], pattern[0]

        for line in pattern:
            left_bound = min(left_bound, line[0])
            right_bound = max(right_bound, line[0])

            lower_bound = min(lower_bound, line[1])
            upper_bound = max(upper_bound, line[1])

        return right_bound - left_bound + 1, upper_bound - lower_bound + 1


if __name__ == '__main__':
    print(PatternRLE.rle([(2, 0), (0, 1), (2, 1), (1, 2), (2, 2)]),
          PatternRLE.rle([(1, 0), (2, 0), (3, 0), (0, 1), (1, 2), (2, 2)]))

    print(PatternRLE.file_to_pat('gosper.rle'))
