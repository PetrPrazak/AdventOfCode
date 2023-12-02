# https://adventofcode.com/2023/day/1
from pathlib import Path
import time


worddigits = ["one", "two", "three", "four",
              "five", "six", "seven", "eight",  "nine"]

num_word = {w: i+1 for i, w in enumerate(worddigits)}

def get_nums(word, part2=False):
    nums = []
    for pos, c in enumerate(word):
        if c.isdigit():
            nums.append(int(c))
        if part2:
            for num, val in num_word.items():
                if word[pos:].startswith(num):
                    nums.append(val)
    return nums


def calibration(nums):
    return nums[0] * 10 + nums[-1]


def process(data):
    # part 1
    result = sum(calibration(get_nums(d)) for d in data)
    print("part 1:", result)
    # part 2
    result = sum(calibration(get_nums(d, part2=True)) for d in data)
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
    # main("test2.txt")
    main()
