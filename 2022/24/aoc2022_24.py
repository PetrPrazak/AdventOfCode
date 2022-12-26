# https://adventofcode.com/2022/day/24
from pathlib import Path
import time


# bits for directions
EMPTY, LEFT, RIGHT, UP, DOWN = 0, 1, 2, 4, 8
BLIZZARD = {"<": LEFT, ">": RIGHT, "^": UP, "v": DOWN, ".": EMPTY}
DIR = {LEFT: -1, RIGHT: 1, UP: -1j, DOWN: 1j}
MOVES = tuple(DIR.values())


def make_state(data):
    width, height = len(data[0]) - 2, len(data) - 2
    state = {
        (col + row * 1j): BLIZZARD[c]
        for row, line in enumerate(data[1:-1])
        for col, c in enumerate(line[1:-1])
    }
    return state, (width, height)


def new_pos(pos, width, height, off):
    pos += off
    col, row = pos.real % width, pos.imag % height
    return col + row * 1j


def move_blizzards(state, width, height):
    new_state = {}
    for pos, winds in state.items():
        for d, off in DIR.items():
            if winds & d:
                npos = new_pos(pos, width, height, off)
                new_state[npos] = new_state.get(npos, 0) | d
    return new_state


def is_free(state, width, height, pos):
    col, row = pos.real, pos.imag
    return col in range(width) and row in range(height) and pos in state


def neighbors(state, width, height, pos):
    # above entry point
    if pos == 0:
        yield -1j
    # above exit point
    elif pos == (width - 1) + (height - 1) * 1j:
        yield pos + 1j
    yield from (pos + off for off in MOVES if is_free(state, width, height, pos + off))
    # wait possibility
    if pos not in state:
        yield pos


def walk_blizzards(state, width, height, start, end):
    positions, time = {start}, 0
    while end not in positions:
        time += 1
        state = move_blizzards(state, width, height)
        new_positions = set()
        for pos in positions:
            neigh = neighbors(state, width, height, pos)
            new_positions.update(neigh)
        positions = new_positions
    return time, state


def process(data):
    # part 1
    state, (width, height) = make_state(data)
    start, end = -1j, width - 1 + height * 1j
    result, state = walk_blizzards(state, width, height, start, end)
    print("part 1:", result)
    # part 2
    back, state = walk_blizzards(state, width, height, end, start)
    there, state = walk_blizzards(state, width, height, start, end)
    result += back + there
    print("part 2:", result)


def load_data(fileobj):
    return [line.rstrip() for line in fileobj.readlines()]


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
