# https://adventofcode.com/2023/day/4
from pathlib import Path
from collections import defaultdict
import time


def process(data):
    p1total = 0
    copies = defaultdict(int)
    for card, (win, have) in enumerate(data):
        same_numbers = len(win & have)
        # part 1
        p1total += 1 << same_numbers >> 1  # handles the zero case as well
        # part 2
        copies[card] += 1
        if same_numbers:
            for won_card in range(card + 1, min(len(data), card + same_numbers + 1)):
                copies[won_card] += copies[card]
    p2total = sum(copies.values())
    print("part 1:", p1total)
    print("part 2:", p2total)


def parse_line(line):
    _, nums = line.split(": ")
    win, have = nums.split(' | ')
    return set(map(int, win.split())), set(map(int, have.split()))


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
