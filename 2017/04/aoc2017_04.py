# https://adventofcode.com/2017/day/4
from __future__ import print_function


def solve(lines, part):
    sum = 0
    for line in lines:
        d = dict()
        valid = True
        for word in line.split():
            if part == 2:
                word = "".join(sorted(word))
            if word in d:
                valid = False
                break
            d[word] = word
        if valid:
            sum += 1
    print(sum)


def better_solve(lines, part):
    asum = 0
    for line in lines:
        l = line.split()
        if part == 2:
            l = ["".join(sorted(word)) for word in l]
        if len(l) == len(set(l)):
            asum += 1
    print(asum)


if __name__ == "__main__":
    with open("input.txt") as f:
        thelines = f.readlines()
        better_solve(thelines, 1)
        better_solve(thelines, 2)
