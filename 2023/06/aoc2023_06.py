# https://adventofcode.com/2023/day/6
from pathlib import Path
from math import prod, sqrt, ceil, floor
import time


# naive solution
def count_ways_to_win_naive(total_time, distance):
    ways = 0
    for button_time in range(total_time):
        boat_dist = (total_time - button_time) * button_time
        if boat_dist > distance:
            ways += 1
    return ways


# quadratic equation solution
def count_ways_to_win_quadratic(total_time, distance):
    delta = sqrt(total_time ** 2 - 4 * distance)
    xmin, xmax = (total_time - delta) / 2, (total_time + delta) / 2
    return ceil(xmax) - floor(xmin) - 1


count_ways_to_win = count_ways_to_win_quadratic


def process(data):
    # part 1
    result = prod(map(count_ways_to_win, *data))
    print("part 1:", result)
    # part 2
    new_t = int(''.join(str(n) for n in data[0]))
    new_d = int(''.join(str(n) for n in data[1]))
    result = count_ways_to_win(new_t, new_d)
    print("part 2:", result)


def parse_line(line):
    return [int(n) for n in line.split()[1:]]


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
