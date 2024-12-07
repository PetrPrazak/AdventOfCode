# https://adventofcode.com/2024/day/7
from pathlib import Path
import time
from math import log10

def join(a, b): return a * 10 ** int(log10(b) + 1) + b


def try_operators(res, nums, part=1):
    stack = [nums[0]]
    for n in nums[1:]:
        newstack = []
        for r in stack:
            rplus = r + n
            if rplus <= res:
                newstack.append(rplus)
            rmul = r * n
            if rmul <= res:
                newstack.append(rmul)
            if part == 2:
                rconcat = join(r, n)
                if rconcat <= res:
                    newstack.append(rconcat)
        stack = newstack
    return res in stack


def process(data):
    # part 1
    result = 0
    rest = []
    for res, nums in data:
        if try_operators(res, nums):
            result += res
        else:
            rest.append((res, nums))
    print("part 1:", result)

    # part 2
    result += sum(res for res, nums in rest if try_operators(res, nums, part=2))
    print("part 2:", result)


def parse_line(line):
    result, nums = line.split(': ')
    nums = list(map(int, nums.split()))
    return int(result), nums


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
    # main("test.txt")
    main()
