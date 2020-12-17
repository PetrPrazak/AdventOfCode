# https://adventofcode.com/2020/day/17
from __future__ import print_function
from functools import cache
from itertools import product


@cache
def gen_offsets(dim):
    offsets = list(product([-1, 0, 1], repeat=dim))
    offsets.remove(tuple([0]*dim))
    return offsets


def get_new_state(grid, pos):
    total = 0
    dimensions = len(pos)
    for diff in gen_offsets(dimensions):
        neighbor = tuple([pos[dim] + diff[dim] for dim in range(dimensions)])
        total += int(neighbor in grid)
        if total > 3:
            return False
    if pos in grid:
        return total == 2 or total == 3
    else:
        return total == 3


def get_size(grid, dim):
    min_pos, max_pos = [0] * dim, [0] * dim
    for pos in grid:
        for d in range(dim):
            min_pos[d] = min(pos[d], min_pos[d])
            max_pos[d] = max(pos[d], max_pos[d])
    return list(zip(min_pos, max_pos))


def gen_pos(size, margin=1):
    first, *rest = size
    for n in range(first[0]-margin, first[1]+1+margin):
        if rest:
            for t in gen_pos(rest, margin):
                yield (n,) + t
        else:
            yield (n,)


def grid_cycle(grid, dim):
    size = get_size(grid, dim)
    new_grid = {pos for pos in gen_pos(size) if get_new_state(grid, pos)}
    return new_grid


def print_grid(grid, dim):
    X, Y, *rest = get_size(grid, dim)
    for r in gen_pos(rest, 0):
        print(f"{r}")
        for y in range(Y[0], Y[1]+1):
            line = []
            for x in range(X[0], X[1]+1):
                line.append('#' if (x, y) + r in grid else '.')
            print(''.join(line))
        print()
    pass


def sum_grid(grid):
    # we keep only active states
    return len(grid)


def cycle_grid(grid, dim, steps):
    for _ in range(steps):
        grid = grid_cycle(grid, dim)
    return sum_grid(grid)


def init_grid(data, dim):
    grid = set()
    for y, line in enumerate(data):
        for x, state in enumerate(line):
            if state == '#':
                grid.add((x, y) + tuple([0] * (dim - 2)))
    return grid


def process(data):
    # part 1
    grid = init_grid(data, 3)
    result = cycle_grid(grid, 3, 6)
    print("part 1:", result)
    # part 2
    grid = init_grid(data, 4)
    result = cycle_grid(grid, 4, 6)
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
