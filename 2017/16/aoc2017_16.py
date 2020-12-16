# http://adventofcode.com/2017/day/16
from __future__ import print_function

# s1, a spin of size 1: eabcd.
# x3/4, swapping the last two programs: eabdc.
# pe/b, swapping programs e and b: baedc.

# make the script version agnostic
try:
    xrange
except NameError:
    xrange = range


def solve(data):
    moves = data.strip().split(',')
    dance(1, moves)
    dance(1000000000, moves)


def dance(reps, moves):
    row = [chr(ord('a') + x) for x in range(16)]
    positions = []
    for i in xrange(reps):
        s = "".join(row)
        if s in positions:
            print(i, positions[reps % i])
            return
        positions.append(s)
        for m in moves:
            if m[0] == 's':
                c = int(m[1:])
                row = row[-c:] + row[:-c]
            elif m[0] == 'x':
                x, y = map(int, m[1:].split('/'))
                row[x], row[y] = row[y], row[x]
            elif m[0] == 'p':
                x, y = m[1:].split('/')
                a = row.index(x)
                b = row.index(y)
                row[a], row[b] = row[b], row[a]
    print("".join(row))


if __name__ == "__main__":
    with open("input.txt") as f:
        # read all in once
        data = f.read()
        solve(data)
