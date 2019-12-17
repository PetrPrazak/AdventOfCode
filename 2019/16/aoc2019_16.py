# https://adventofcode.com/2019/day/16
from __future__ import print_function
from functools import reduce
from itertools import cycle, repeat, islice
import pathlib
import sys
from operator import add, mul

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))
from aoc import *

INPUT = "aoc2019_16_input.txt"
TEST = "test.txt"


def parse_code(data):
    code = [int(c) for c in data]
    return code


def string_code(code):
    return cat([str(d) for d in code])


def get_phase(idx):
    base = [1, -1]
    for b in cycle(base):
        yield b


def repeat_times(iterable, times=1):
    for _ in range(times):
        for item in iterable:
            yield item


def repeat_times_skip(iterable, skip=0, times=1):
    return islice(repeat_times(iterable, times), skip, None)


def calc_digit(code, idx):
    accum = 0
    pos = idx
    phase = get_phase(idx)
    while pos < len(code):
        p = next(phase)
        accum += sum(code[pos:pos + idx + 1]) * p
        pos += 2 * (idx + 1)
    newdigit = abs(accum) % 10
    return newdigit


def run_phase(code):
    out = [calc_digit(code, idx) for idx, digit in enumerate(code)]
    return out


@timeit
def part1(data, runs=100):
    # part 1
    code = parse_code(data)
    for _ in range(runs):
        code = run_phase(code)
    ret = code[:8]
    return ret


@timeit
def part2(data, runs=100, times=10000):
    # part 2
    code = parse_code(data)
    msg_offset = int(data[:7])
    code = code * times
    assert msg_offset > len(code) // 2
    code = code[msg_offset:]
    for i in range(runs):
        rev_sum = code[-1:]
        for x in code[-2::-1]:
            rev_sum.append(rev_sum[-1] + x)
        code = [abs(x) % 10 for x in reversed(rev_sum)]
    return code[:8]


def test():
    # assert string_code(part1("12345678", 4)) == "01029498"
    # assert string_code(part1("69317163492948606335995924319873", 100)) == "52432133"
    part2("03036732577212944063491565474664")


def main():
    data = read_input_line(INPUT)
    print(string_code(part1(data)))
    print(string_code(part2(data)))



if __name__ == "__main__":
    # test1()
    # test()
    main()
