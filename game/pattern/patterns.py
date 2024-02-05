class PatternBase:
    def __init__(self):
        self.alive_cells = set()

    @property
    def bbox(self):
        return None

    def translate(self, pos: tuple[int, int]):
        pass

    def translated(self, pos: tuple[int, int]):
        pass

    def strip(self):
        pass

    def stripped(self):
        pass

    def add(self, pattern, pos: tuple[int, int]):
        pass

    def clear_rect(self, x, y, w, h):
        pass


class Pattern(PatternBase):
    def __init__(self, p=None):
        super().__init__()
        if p is None:
            self.alive_cells = set()
        elif isinstance(p, str):  # for RLE pattern
            self.alive_cells: set[tuple[int, int]] = set(Pattern.rle_to_pat(p))
        elif isinstance(p, self.__class__):  # for Pattern objects
            self.alive_cells = set(p.alive_cells)
        elif hasattr(p, '__iter__'):
            self.alive_cells = set(p)

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

        return left_bound, lower_bound, right_bound - left_bound + 1, upper_bound - lower_bound + 1

    def copy(self):
        return Pattern(self.alive_cells)

    def translate(self, pos: tuple[int, int]):
        new_cells = {(x[0] + pos[0], x[1] + pos[1]) for x in self.alive_cells}
        self.alive_cells = new_cells

    def translated(self, pos: tuple[int, int]):
        return Pattern({(x[0] + pos[0], x[1] + pos[1]) for x in self.alive_cells})

    def strip(self):
        x, y, _, _ = self.bounding_box
        self.translate((-x, -y))

    def stripped(self):
        x, y, _, _ = self.bounding_box
        return self.translated((-x, -y))

    def add(self, pattern, pos: tuple[int, int] | None = None):
        """
        Adds the Pattern object, pattern, with top-left corner at position, pos, and returns resulting pattern.
        :param pattern: Pattern
        :param pos: tuple[int, int]
        :return: Pattern
        """
        assert isinstance(pattern, self.__class__)

        if pos is None:
            pos = (0, 0)

        self.alive_cells |= pattern.translated(pos).alive_cells

    def clear_rect(self, x, y, w, h):
        """
        Clears all alive cells in the rectangle, rect (left-top-x, left-top-y, width-w, height-h).
        Returns resulting pattern.
        :return: Pattern
        """

        positions = {(a, b) for a in range(x, x + w) for b in range(y, y + h)}
        self.alive_cells -= positions

    def rotate90(self, clockwise=True):
        x, y, w, h = self.bounding_box

        if clockwise:
            self.alive_cells = {(-y, x) for (x, y) in self.alive_cells}
            self.translate((h - 1, 0))
        else:
            self.alive_cells = {(y, -x) for (x, y) in self.alive_cells}
            self.translate((0, w - 1))

    def flip_x(self):
        x, y, w, h = self.bounding_box
        self.alive_cells = {(x, -y) for (x, y) in self.alive_cells}
        self.translate((0, h - 1))

    def flip_y(self):
        x, y, w, h = self.bounding_box
        self.alive_cells = {(-x, y) for (x, y) in self.alive_cells}
        self.translate((w - 1, 0))

    def to_rle(self):
        return Pattern.pat_to_rle(list(self.alive_cells))

    @staticmethod
    def open(file, encoding='rle'):
        with open(file) as f:
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
