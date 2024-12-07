# https://adventofcode.com/2024/day/7
from pathlib import Path
import time
from math import log10


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
                rconcat = r * 10 ** int(log10(n) + 1) + n
                if rconcat <= res:
                    newstack.append(rconcat)
        stack = newstack
    return res in stack


# much faster recursive solution, process the list backwards
def check_nums(res, nums, part=1):
    if len(nums) == 1:
        return res == nums[0]
    last, rest = nums[-1], nums[:-1]
    if res % last == 0 and check_nums(res // last, rest, part):
        return True
    if res > last and check_nums(res - last, rest, part):
        return True
    if part == 2:
        s_res, s_last = str(res), str(last)
        if len(s_res) > len(s_last) and s_res.endswith(s_last) \
                and check_nums(int(s_res[:-len(s_last)]), rest, part):
            return True
    return False


def process(data):
    # part 1
    result = sum(res for res, nums in data if check_nums(res, nums))
    print("part 1:", result)

    # part 2
    result = sum(res for res, nums in data if check_nums(res, nums, part=2))
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
