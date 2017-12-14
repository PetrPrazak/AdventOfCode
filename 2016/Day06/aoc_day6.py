from __future__ import print_function
from collections import Counter, defaultdict


def solve(lines, part=1):

    cnt = []
    for line in lines:
        line = line.strip()
        if not cnt:
            for i in range(len(line)):
                cnt.append(Counter())

        for pos,c in enumerate(list(line)):
            cnt[pos][c] += 1

    print("".join([a.most_common(1)[0][0] for a in cnt]))
    print("".join([a.most_common()[-1][0] for a in cnt])) #part 2


# INPUT = "aoc_day6_test.txt"
INPUT = "aoc_day6_input.txt"

if __name__ == "__main__":
    with open(INPUT) as f:
       l = f.readlines()
    solve(l,2)
