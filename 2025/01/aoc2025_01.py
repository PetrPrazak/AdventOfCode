# https://adventofcode.com/2025/day/1
from pathlib import Path
import time


def part1(data, pos=50):
    passwd = 0
    for rotations, directions in data:
        pos = (pos + rotations * directions) % 100
        if pos == 0:
            passwd += 1
    return passwd


def part2(data, pos=50):
    passwd = 0
    for rotations, direction in data:
        circles, rotations = divmod(rotations, 100)
        passwd += circles
        newpos = pos + rotations * direction
        if newpos <= 0 and pos != 0:
            passwd += 1
        elif newpos >= 100:
            passwd += 1
        pos = newpos % 100

    return passwd


def process(data):
    # part 1
    result = part1(data)
    print("part 1:", result)
    # part 2
    result = part2(data)
    print("part 2:", result)


def parse_line(line):
    return int(line[1:]), (-1 if line[0] == 'L' else 1)


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
