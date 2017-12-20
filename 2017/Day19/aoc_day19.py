"""

http://adventofcode.com/2017/day/19


"""
from __future__ import print_function


def solve(lines):
    # init
    maxlen = max(len(line) for line in lines)
    chart = [list(line.strip('\n') + " " * (maxlen - len(line))) for line in lines]

    path = ""
    x, y = chart[0].index('|'), 0
    dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    direction = 2  # south
    steps = 1
    while True:
        # calculate next position
        dx, dy = dirs[direction]
        x, y = x + dx, y + dy

        row = chart[y]
        char = row[x]

        if char == "|" or char == "-":
            pass
        elif char == "+":
            # determine new direction
            if direction == 0 or direction == 2:
                n = row[x - 1]
                direction = 3 if n == "-" or n.isalpha() else 1
            else:
                n = chart[y - 1][x]
                direction = 0 if n == "|" or n.isalpha() else 2
        elif char == ' ':
            # line stopped
            break
        else:
            path += char

        steps += 1

    print(steps, path)


INPUT = "aoc_day19_input.txt"
# INPUT = "aoc_day19_test.txt"


def main():
    with open(INPUT) as f:
        # read by lines
        lines = f.readlines()
        solve(lines)


if __name__ == "__main__":
    main()
