# https://adventofcode.com/2025/day/7
from pathlib import Path
from collections import defaultdict
import time


def part1_and_2(splitters, start, rows):
    beams = {start[1]: 1}
    acc = 0
    for row in range(start[0], rows):
        next_beams = defaultdict(int)
        for beam_col, val in beams.items():
            if beam_col in splitters[row]:
                acc += 1
                next_beams[beam_col - 1] += val
                next_beams[beam_col + 1] += val
            else:
                next_beams[beam_col] += val
        beams = next_beams
    return acc, sum(beams.values())


def process(data):
    splitters = defaultdict(set)
    start = None
    for row, items in enumerate(data):
        for col, c in items:
            if c == 'S':
                start = row, col
            else:
                splitters[row].add(col)

    # part 1 and 2 together
    result = part1_and_2(splitters, start, len(data))
    print("part 1:", result[0])
    print("part 2:", result[1])


def parse_line(line):
    return [(i, c) for i, c in enumerate(line) if c != '.']


def load_data(fileobj):
    return [parse_line(line.rstrip()) for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        t1 = time.perf_counter()
        process(load_data(f))
        t2 = time.perf_counter()
        print(f"Finished in {t2 - t1:.3f} s")


if __name__ == "__main__":
    main("test.txt")
    main()
