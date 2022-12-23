# https://adventofcode.com/2022/day/22
from pathlib import Path
import time


def make_grid(data):
    grid = {
        (x + y * 1j): char
        for y, row in enumerate(data)
        for x, char in enumerate(row)
        if char != " "
    }
    start_pos = min(x.real for x in grid if x.imag == 0)
    return grid, start_pos


def wrap_pos(grid, pos, facing):
    pos += facing
    if pos in grid:
        return pos
    dcol, drow = facing.real, facing.imag
    col, row = pos.real, pos.imag
    if dcol:
        fn = min if dcol == 1 else max
        col = fn(p.real for p in grid if p.imag == row)
    if drow:
        fn = min if drow == 1 else max
        row = fn(p.imag for p in grid if p.real == col)
    return col + row * 1j


def get_plane(size, pos):
    width, cols = size
    plane_col, plane_row = pos.real // width, pos.imag // width
    plane = plane_col + plane_row * cols
    return int(plane)


def plane_start_pos(size, plane):
    width, cols = size
    r, c = divmod(plane, cols)
    return (c + r * 1j) * width


def noop_pos(size, plane, pos):
    width = size[0]
    row, col = pos.imag % width, pos.real % width
    return plane_start_pos(size, plane) + (col + row * 1j)


def rotr_pos(size, plane, pos):
    width = size[0]
    col, row = width - 1 - pos.imag % width, pos.real % width
    return plane_start_pos(size, plane) + (col + row * 1j)


def rotl_pos(size, plane, pos):
    width = size[0]
    col, row = pos.imag % width, width - 1 - pos.real % width
    return plane_start_pos(size, plane) + (col + row * 1j)


def rot2_pos(size, plane, pos):
    width = size[0]
    row, col = width - 1 - pos.imag % width, width - 1 - pos.real % width
    return plane_start_pos(size, plane) + (col + row * 1j)


RIGHT, DOWN, LEFT, UP = 1 + 0j, 1j, -1 + 0j, -1j
# Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^).
FACING = [RIGHT, DOWN, LEFT, UP]


def example_cube(cur_plane, next_plane):
    A, B, C, D, E, F = 2, 4, 5, 6, 10, 11
    CUBE = {
        A: {-2: (B, rot2_pos, DOWN), 1: (C, rotl_pos, DOWN), 3: (F, rot2_pos, DOWN)},
        B: {0: (A, rot2_pos, DOWN), 3: (F, rotr_pos, UP), 8: (E, rot2_pos, UP)},
        C: {1: (A, rotr_pos, RIGHT), 9: (E, rotl_pos, RIGHT)},
        D: {7: (F, rotr_pos, DOWN)},
        E: {9: (C, rotr_pos, UP), 14: (B, rot2_pos, UP)},
        F: {7: (D, rotl_pos, LEFT), 12: (A, rot2_pos, LEFT), 15: (B, rotl_pos, RIGHT)},
    }
    return CUBE[cur_plane].get(next_plane)


def input_cube(cur_plane, next_plane):
    A, B, C, D, E, F = 1, 9, 6, 4, 7, 2
    CUBE = {
        A: {-2: (B, rotr_pos, RIGHT), 0: (C, rot2_pos, RIGHT)},
        B: {8: (A, rotl_pos, DOWN), 10: (E, rotl_pos, UP), 12: (F, noop_pos, DOWN)},
        C: {3: (D, rotr_pos, RIGHT), 5: (A, rot2_pos, RIGHT)},
        D: {3: (C, rotl_pos, DOWN), 5: (F, rotl_pos, UP)},
        E: {8: (F, rot2_pos, LEFT), 10: (B, rotr_pos, LEFT)},
        F: {-1: (B, noop_pos, UP), 3: (E, rot2_pos, LEFT), 5: (D, rotr_pos, LEFT)},
    }
    return CUBE[cur_plane].get(next_plane)


def cube_wrap_pos(size, pos, facing):
    mapping = input_cube if size[0] == 50 else example_cube
    cur_plane = get_plane(size, pos)
    pos += facing
    next_plane = get_plane(size, pos)
    if cur_plane == next_plane:
        return pos, facing
    m = mapping(cur_plane, next_plane)
    if m is None:
        return pos, facing
    act_plane, trans_pos, facing = m
    return trans_pos(size, act_plane, pos), facing


def walk_grid(grid, start_pos, path, part=1):
    facing = 1 + 0j
    pos = start_pos
    width = int(max(p.real for p in grid) + 1)
    height = int(max(p.imag for p in grid) + 1)
    cols = 3 if width < height else 4
    size = width // cols, cols
    print(f"{size=}")
    for step in path:
        if step == "R" or step == "L":
            facing *= 1j if step == "R" else -1j
        else:
            step = int(step)
            while step > 0:
                if part == 1:
                    next_pos = wrap_pos(grid, pos, facing)
                    next_facing = facing
                else:
                    next_pos, next_facing = cube_wrap_pos(size, pos, facing)
                if grid[next_pos] == "#":
                    break
                facing = next_facing
                pos = next_pos
                step -= 1
    return pos.real, pos.imag, FACING.index(facing)


def password(col, row, facing):
    return int(4 * (col + 1) + 1000 * (row + 1) + facing)


def process(data):
    # part 1
    map, path = data
    print(len(path))
    grid, start_pos = make_grid(map)
    result = password(*walk_grid(grid, start_pos, path))
    print("part 1:", result)
    # part 2
    result = password(*walk_grid(grid, start_pos, path, part=2))
    print("part 2:", result)


def parse_path(path):
    path = path.replace("R", " R ").replace("L", " L ")
    return tuple(path.split())


def load_data(fileobj):
    grid, path = fileobj.read().split("\n\n")
    return [l.rstrip() for l in grid.split("\n")], parse_path(path.rstrip())


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        t1 = time.perf_counter()
        process(load_data(f))
        t2 = time.perf_counter()
        print(f"Finished in {t2 - t1:.3} s")


if __name__ == "__main__":
    # main("test.txt")
    main()
