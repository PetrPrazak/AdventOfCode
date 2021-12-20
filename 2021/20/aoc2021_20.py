# https://adventofcode.com/2021/day/20
from __future__ import print_function
from pathlib import Path
from operator import itemgetter


def minmax_tuples(tuple_list, element=0):
    res = sorted(tuple_list, key=itemgetter(element))
    return res[0][element], res[-1][element]


def make_grid(data):
    return {(x, y)
            for y in range(len(data))
            for x in range(len(data[y]))
            if data[y][x] == '#'}


def pixel_box(point):
    x, y = point
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            yield x+dx, y+dy


def enhance_grid(algo, grid, default):
    def enhance_pixel(algo, grid, default, pos):
        idx = 0
        for x, y in pixel_box(pos):
            idx <<= 1
            idx |= ((x, y) in grid) or (
                default and (x < min_x or x > max_x or y < min_y or y > max_y))
        return algo[idx]

    min_x, max_x = minmax_tuples(grid, 0)
    min_y, max_y = minmax_tuples(grid, 1)
    new_grid = {(x, y)
                for y in range(min_y - 1, max_y + 2)
                for x in range(min_x - 1, max_x + 2)
                if enhance_pixel(algo, grid, default, (x, y))}
    return new_grid


def loop_enhance(algo, grid, count=2):
    for i in range(count):
        grid = enhance_grid(algo, grid, algo[0] and i % 2 == 1)
    return grid


def process(data):
    algo, grid_def = data[0], data[2:]
    # part 1
    algo = tuple(x == '#' for x in algo)
    assert not (algo[0] and algo[-1]), "invalid input, will lit all image!"
    grid = make_grid(grid_def)
    grid = loop_enhance(algo, grid)
    print("part 1:", len(grid))
    # part 2
    grid = loop_enhance(algo, grid, 48)
    print("part 2:", len(grid))


def load_data(fileobj):
    return [line.strip() for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
