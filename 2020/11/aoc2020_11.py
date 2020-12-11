# https://adventofcode.com/2020/day/11
from __future__ import print_function
from itertools import product


def sum_grid(grid):
    return sum(int(c == '#') for line in grid for c in line)


offsets = list(product([-1, 0, 1], [-1, 0, 1]))
offsets.remove((0, 0))


def get_state_part1(grid, height, width, x, y):
    if grid[y][x] == '.':
        return '.'
    total_occupied = 0
    for dif_x, dif_y in offsets:
        neighbor_x = x + dif_x
        neighbor_y = y + dif_y
        if neighbor_x not in range(width) or neighbor_y not in range(height):
            continue
        total_occupied += int(grid[neighbor_y][neighbor_x] == '#')
    state = grid[y][x]
    if state == 'L':
        return '#' if total_occupied == 0 else state
    else:
        return 'L' if total_occupied >= 4 else state


def get_state_part2(grid, height, width, x, y):
    if grid[y][x] == '.':
        return '.'
    total_occupied = 0
    for dif_x, dif_y in offsets:
        neighbor_x = x + dif_x
        neighbor_y = y + dif_y
        while True:
            if neighbor_x not in range(width) or neighbor_y not in range(height):
                break
            if grid[neighbor_y][neighbor_x] == '#':
                total_occupied += 1
                break
            if grid[neighbor_y][neighbor_x] == 'L':
                break
            neighbor_x += dif_x
            neighbor_y += dif_y

    state = grid[y][x]
    if state == 'L':
        return '#' if total_occupied == 0 else state
    else:
        return 'L' if total_occupied >= 5 else state


def grid_cycle(grid, get_state):
    height, width = len(grid), len(grid[0])
    new_grid = [[get_state(grid, height, width, x, y) for x in range(width)]
                for y in range(height)]
    return new_grid


def grid_equal(grid1, grid2):
    return all(l == r for l, r in zip(grid1, grid2))


def loop_grid(grid, steps, get_state):
    for _ in range(steps):
        newgrid = grid_cycle(grid, get_state)
        if grid_equal(grid, newgrid):
            return sum_grid(grid)
        grid = newgrid
    return None


def process(data):
    # part 1
    result = loop_grid(data, 1000, get_state_part1)
    print("part 1:", result)
    # part 2
    result = loop_grid(data, 1000, get_state_part2)
    print("part 2:", result)


def load_data(fileobj):
    return [list(line.rstrip()) for line in fileobj]


def main(file):
    print(file)
    with open(file) as f:
        process(load_data(f))


if __name__ == "__main__":
    main("test.txt")
    main("input.txt")
