# https://adventofcode.com/2023/day/16
from pathlib import Path
from collections import deque
import time

UP, DOWN, LEFT, RIGHT = -1+0j, 1+0j, -1j, 1j


def next_pos(data, pos, direction):

    rows, cols = len(data), len(data[0])

    def next_valid_pos(pos, d):
        pos += d
        if pos.real in range(0, rows) and pos.imag in range(0, cols):
            yield pos, d

    x, y = int(pos.real), int(pos.imag)
    dx, dy = int(direction.real), int(direction.imag)
    cell = data[x][y]
    if cell == '\\' or cell == '/':
        # turn the beam
        d = direction * (RIGHT if (dx != 0) ^ (cell == '/') else LEFT)
        yield from next_valid_pos(pos, d)
    elif cell == '-' and dx:
        # split left and right
        yield from next_valid_pos(pos, LEFT)
        yield from next_valid_pos(pos, RIGHT)
    elif cell == '|' and dy:
        # split down and up
        yield from next_valid_pos(pos, DOWN)
        yield from next_valid_pos(pos, UP)
    else:
        # keep going
        yield from next_valid_pos(pos, direction)


def walk(data, start=0j, direction=1j):
    pos = start, direction
    visited = {pos}
    q = deque([pos])
    while q:
        pos = q.popleft()
        for nextpos in next_pos(data, *pos):
            if nextpos not in visited:
                visited.add(nextpos)
                q.append(nextpos)
    return len({p for p, _ in visited})


def try_edges(data):
    energized = 0
    rows, cols = len(data), len(data[0])
    for r in range(rows):
        pos = r + 0j
        energized = max(energized, walk(data, pos, RIGHT))
        energized = max(energized, walk(data, pos + (cols-1)*1j, LEFT))
    for c in range(cols):
        pos = 1j * c
        energized = max(energized, walk(data, pos, DOWN))
        energized = max(energized, walk(data, pos + (rows-1), UP))
    return energized


def process(data):
    # part 1
    result = walk(data)
    print("part 1:", result)
    # part 2
    result = try_edges(data)
    print("part 2:", result)


def load_data(fileobj):
    return [list(line.rstrip()) for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        t1 = time.perf_counter()
        process(load_data(f))
        t2 = time.perf_counter()
        print(f"Finished in {t2 - t1:.3f} s")


if __name__ == "__main__":
    # main("test.txt")
    main()
