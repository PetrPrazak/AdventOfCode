# https://adventofcode.com/2023/day/13
from pathlib import Path
from operator import eq
import time


def is_mirrored(pattern, row, compare):
    up, down = row, row + 1
    while up >= 0 and down < len(pattern):
        if not compare(pattern[up], pattern[down]):
            return False
        up -= 1
        down += 1
    return True


def smudge_compare(line1, line2):
    global had_smudge
    if had_smudge:
        return line1 == line2
    s = sum(c != d for c, d in zip(line1, line2))
    if s == 1:
        if had_smudge:
            return False
        had_smudge = True
    return s <= 1


def mirror_line(pattern, compare, part=1):
    global had_smudge
    for r, (l1, l2) in enumerate(zip(pattern, pattern[1:])):
        had_smudge = False
        if is_mirrored(pattern, r, compare):
            if part == 1 or had_smudge:
                return r + 1
    return 0


def score(idx, pattern, compare=eq, part=1):
    s = mirror_line(pattern, compare, part) * 100
    if not s:
        s = mirror_line(list(zip(*pattern)), compare, part)
    if not s:
        print(f"Pattern {idx} has no mirror!")
    return s


def process(data):
    # part 1
    result = sum(score(*d) for d in enumerate(data))
    print("part 1:", result)
    # part 2
    result = sum(score(*d, compare=smudge_compare, part=2)
                 for d in enumerate(data))
    print("part 2:", result)


def parse_section(section):
    return list(section.split("\n"))


def load_data(fileobj):
    return [parse_section(part) for part in fileobj.read().split("\n\n")]


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
