# https://adventofcode.com/2017/day/5
from __future__ import print_function


def solve(lines, part):
    IP = 0

    jumps = [int(l) for l in lines]
    steps = 0
    end = len(jumps)
    while 0 <= IP < end:
        offset = jumps[IP]
        newIP = IP + offset
        if part == 2 and offset >= 3:
            jumps[IP] -= 1
        else:
            jumps[IP] += 1
        IP = newIP
        steps += 1

    print(steps)


if __name__ == "__main__":
    with open("input.txt") as f:
        thelines = f.readlines()
        solve(thelines, 1)
        solve(thelines, 2)
