# https://adventofcode.com/2018/day/14

from __future__ import print_function

cat = ''.join


def process(recipies):
    space = [3, 7]
    first, second = 0, 1

    while len(space) < recipies + 10:
        r1, r2 = space[first], space[second]
        new = r1 + r2
        dec, rem = new // 10, new % 10
        if dec:
            space.append(dec)
        space.append(rem)
        first = (first + r1 + 1) % len(space)
        second = (second + r2 + 1) % len(space)

    return space[recipies:recipies + 10]


def process2(seq):
    space = [3, 7]
    first, second = 0, 1
    seq_len = len(seq)

    while True:
        r1, r2 = space[first], space[second]
        new = r1 + r2
        dec, rem = new // 10, new % 10
        if dec:
            space.append(dec)
        space.append(rem)
        first = (first + r1 + 1) % len(space)
        second = (second + r2 + 1) % len(space)

        if len(space) > seq_len:
            if space[-seq_len:] == seq or space[-seq_len - 1:-1] == seq:
                break

    ret = len(space) - seq_len
    if space[-seq_len - 1:-1] == seq:
        ret -= 1
    return ret


INPUT = "330121"
# part 1
ret = process(int(INPUT))
print(cat(list(map(str, ret))))
# part 2
print(process2(list(map(int, INPUT))))
