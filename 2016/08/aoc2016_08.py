# http://adventofcode.com/2016/day/8
from __future__ import print_function
from collections import defaultdict

def print_matrix(matrix, size):
    width, height = size
    for y in range(height):
        line = "".join("#" if matrix[(x, y)] else ' ' for x in range(width))
        print(line)
    print("")


def solve(lines, size):
    width, height = size
    matrix = defaultdict(int)

    for parts in lines:
        # rect 20x1
        if parts[0] == "rect":
            addr = parts[1].split('x')
            for x in range(int(addr[0])):
                for y in range(int(addr[1])):
                    matrix[x, y] = 1
        # rotate row y=4 by 20
        elif parts[1] == "row":
            row = int(parts[2][2:])
            offset = int(parts[4])
            for _ in range(offset):
                save = matrix[(width-1, row)]
                for x in reversed(range(width-1)):
                    matrix[((x + 1) % width, row)] = matrix[(x, row)]
                matrix[(0, row)] = save
        # rotate column x=47 by 1
        elif parts[1] == "column":
            col = int(parts[2][2:])
            offset = int(parts[4])
            for _ in range(offset):
                save = matrix[(col, height - 1)]
                for y in reversed(range(height-1)):
                    matrix[(col, (y + 1) % height)] = matrix[(col, y)]
                matrix[(col, 0)] = save

    print("Part 1:", sum(matrix[x] for x in matrix))
    print("Part 2")
    print_matrix(matrix, size)


def main(file):
    with open(file) as f:
        data = [line.strip().split() for line in f.readlines()]
        solve(data, (50, 6))


if __name__ == "__main__":
    # main("aoc_day8_test.txt")
    main("aoc_day8_input.txt")
