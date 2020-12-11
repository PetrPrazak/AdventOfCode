# http://adventofcode.com/2016/day/6
from __future__ import print_function
from collections import Counter


def solve(lines):
    cnt = [Counter() for _ in range(len(lines[0]))]
    for line in lines:
        for pos, c in enumerate(line):
            cnt[pos][c] += 1

    print("Part 1:", "".join([a.most_common(1)[0][0] for a in cnt]))
    print("Part 2:", "".join([a.most_common()[-1][0] for a in cnt]))


def main(file):
    with open(file) as f:
        l = [l.strip() for l in f.readlines()]
        solve(l)


if __name__ == "__main__":
    # main("aoc_day6_test.txt")
    main("aoc_day6_input.txt")
