# https://adventofcode.com/2021/day/25
from __future__ import print_function
from pathlib import Path
from itertools import count


RIGHT = '>'
DOWN = 'v'
EMPTY = '.'


def make_grid(data):
    return {(x, y): data[y][x]
            for y in range(len(data))
            for x in range(len(data[y])) if data[y][x] != EMPTY}


def do_step(grid, height, width):
    newgrid = dict()
    moves = 0
    # process all cucumbers heading east
    for pos, val in grid.items():
        if val == RIGHT:
            newpos = (pos[0] + 1) % width, pos[1]
            if grid.get(newpos, EMPTY) == EMPTY:
                newgrid[newpos] = val
                moves += 1
            else:
                newgrid[pos] = val
    # now process all cucumbers heading south
    for pos, val in grid.items():
        if val == DOWN:
            newpos = pos[0], (pos[1] + 1) % height
            target = grid.get(newpos, EMPTY)
            if target != DOWN and newgrid.get(newpos, EMPTY) == EMPTY:
                newgrid[newpos] = val
                moves += 1
            else:
                newgrid[pos] = val
    return moves, newgrid


def process(data):
    height, width = len(data), len(data[0])
    # part 1
    grid = make_grid(data)
    for step in count(1):
        moves, grid = do_step(grid, height, width)
        if not moves:
            break
    result = step
    print("part 1:", result)


def load_data(fileobj):
    return [list(line.strip()) for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
