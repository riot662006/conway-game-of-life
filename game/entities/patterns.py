import setuptools
from importlib import resources as impresources

try:
    from . import common_patterns
except ImportError:
    import common_patterns


class Pattern:
    def __init__(self, p: str | list[tuple[int, int]]):
        if type(p) == str:  # for RLE pattern
            self.alive_cells = set(Pattern.rle_to_pat(p))
        else:
            self.alive_cells = p

    @property
    def bounding_box(self):
        """
                Finds the size of the bounding box of the pattern.

                :return: tuple([int, int])
                """

        left_bound, lower_bound, right_bound, upper_bound = 0, 0, 0, 0
        first = True

        for line in self.alive_cells:
            if first:
                (left_bound, lower_bound), (right_bound, upper_bound) = line, line
                first = False
            else:
                left_bound = min(left_bound, line[0])
                right_bound = max(right_bound, line[0])

                lower_bound = min(lower_bound, line[1])
                upper_bound = max(upper_bound, line[1])

        return right_bound - left_bound + 1, upper_bound - lower_bound + 1

    @staticmethod
    def open(file, encoding='rle'):
        inp_file = (impresources.files(common_patterns) / file)

        with inp_file.open("rt") as f:
            pat = ""

            for x in f:
                if x[0] not in '#x':
                    pat += x.strip()

            return Pattern(pat)

    @staticmethod
    def rle_to_pat(p):
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
    def pat_to_rle(pattern: list[tuple]):
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


if __name__ == '__main__':
    print(Pattern.pat_to_rle([(2, 0), (0, 1), (2, 1), (1, 2), (2, 2)]),
          Pattern.pat_to_rle([(1, 0), (2, 0), (3, 0), (0, 1), (1, 2), (2, 2)]))

    print(Pattern.open('gosper.rle').alive_cells)
