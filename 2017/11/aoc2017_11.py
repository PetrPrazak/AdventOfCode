# http://adventofcode.com/2017/day/11
from __future__ import print_function
from collections import defaultdict, Counter
from functools import reduce

#   \ n  /
# nw +--+ ne
#   /    \
# -+      +-
#   \    /
# sw +--+ se
#   / s  \

# solve('se,sw,se,sw,sw')

def gridlen(steps):
    # print(steps)
    x, y, z = 0, 0, 0
    maxl = 0
    l = 0
    for s in steps:
        if s == 's' or s == 'n':
            inc = 1 if s == 's' else -1
            y -= inc
            z += inc
        elif s == 'ne' or s == 'sw':
            inc = 1 if s == 'ne' else -1
            z -= inc
            x += inc
        elif s == 'se' or s == 'nw':
            inc = 1 if s == 'se' else -1
            y -= inc
            x += inc
        l = max(abs(x), abs(y), abs(z))
        maxl = max(l, maxl)

    return (l, maxl)


def solve(data):
    cnt = gridlen(data.split(','))
    print(cnt)


if __name__ == "__main__":
    solve('nw,ne')
    solve('n,n,n,n')
    solve('ne,ne,ne,ne')
    solve('ne,ne,sw,sw')
    solve('ne,ne,s,s')
    solve('se,sw,se,sw,sw')
    with open("input.txt") as f:
        # read all in once
        data = f.read().strip()
        solve(data)
