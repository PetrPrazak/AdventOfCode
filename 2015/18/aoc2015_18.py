# https://adventofcode.com/2015/day/18
from __future__ import print_function
from itertools import product


def sum_grid(grid):
    return sum(int(c == '#') for line in grid for c in line)


offsets = list(product([-1, 0, 1], [-1, 0, 1]))


def get_state(grid, height, width, x, y):
    total = 0
    for dif_x, dif_y in offsets:
        neighbor_x = x + dif_x
        neighbor_y = y + dif_y
        if dif_x == 0 and dif_y == 0 \
                or neighbor_x not in range(width) \
                or neighbor_y not in range(height):
            continue
        total += grid[neighbor_y][neighbor_x] == '#'
        if total > 3:
            return '.'
    state = grid[y][x]
    if state == '#':
        return '#' if total == 2 or total == 3 else '.'
    else:
        return '#' if total == 3 else '.'


def grid_cycle(grid):
    height, width = len(grid), len(grid[0])
    new_grid = [[get_state(grid, height, width, x, y) for x in range(width)]
                for y in range(height)]
    return new_grid


def part1(grid, steps):
    for _ in range(steps):
        grid = grid_cycle(grid)
    return sum_grid(grid)


def set_corners_on(grid):
    grid[0][0] = '#'
    grid[0][-1] = '#'
    grid[-1][0] = '#'
    grid[-1][-1] = '#'


def part2(grid, steps):
    set_corners_on(grid)
    for _ in range(steps):
        grid = grid_cycle(grid)
        set_corners_on(grid)
    return sum_grid(grid)


def process(grid, steps):
    # part 1
    result = part1(grid, steps)
    print("part 1:", result)
    # part 2
    result = part2(grid, steps)
    print("part 2:", result)


def parse_line(line):
    return list(line)


def load_data(fileobj):
    return [parse_line(line.rstrip()) for line in fileobj]


def main(file, steps):
    print(file)
    with open(file) as f:
        process(load_data(f), steps)


if __name__ == "__main__":
    # main("test.txt", 5)
    main("input.txt", 100)
