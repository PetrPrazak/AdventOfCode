# https://adventofcode.com/2024/day/14
from pathlib import Path
from collections import Counter
import time
import re


def count_pos(size, tick, posx, posy, vx, vy):
    x = (posx + vx * tick) % size[0]
    y = (posy + vy * tick) % size[1]
    return x, y


def quadrant(size, pos):
    midx, midy = size[0] // 2, size[1] // 2
    if pos[0] == midx or pos[1] == midy:
        return -1
    match pos[0] < midx, pos[1] < midy:
        case True, True: return 0
        case False, True: return 1
        case False, False: return 2
        case True, False: return 3


def print_map(size, robots):
    for c in range(size[0]):
        print("".join('#' if (r, c) in robots else '·'
                      for r in range(size[1])))
    print()


def process(data, size):
    robots = [count_pos(size, 100, *p) for p in data]
    cnt = Counter(quadrant(size, r) for r in robots)
    # part 1
    result = cnt[0] * cnt[1] * cnt[2] * cnt[3]
    print("part 1:", result)
    # part 2
    for t in range(10000):
        robots = set(count_pos(size, t, *p) for p in data)
        if len(robots) == len(data):
            # print_map(size, srobots)
            break
    print("part 2:", t)


def parse_line(line):
    return list(map(int, re.findall(r"-?\d+", line)))


def load_data(fileobj):
    return [parse_line(line.rstrip()) for line in fileobj.readlines()]


def main(file="input.txt", size=(101, 103)):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        t1 = time.perf_counter()
        process(load_data(f), size)
        t2 = time.perf_counter()
        print(f"Finished in {t2 - t1:.3f} s")


if __name__ == "__main__":
    # main("test.txt", size=(11, 7))
    main()
