# http://adventofcode.com/2016/day/14
from __future__ import print_function
from hashlib import md5
from functools import cache


def get_md5(key):
    return md5(key.encode('ascii')).hexdigest()


@cache
def get_hash(salt, idx):
    key = salt + str(idx)
    return get_md5(key)


@cache
def get_hash_part2(salt, idx):
    seed = get_hash(salt, idx)
    for _ in range(2016):
        seed = get_md5(seed)
    return seed


def has_repeating(line, num, letter=None):
    cur = None
    count = 0
    for c in line:
        if c == cur and (not letter or c == letter):
            count += 1
            if count == num:
                return c
        else:
            cur = c
            count = 1
    return None


def find_keys(salt, get_hash_fn):
    keys = []
    for idx in range(100000):
        c = has_repeating(get_hash_fn(salt, idx), 3)
        if not c:
            continue
        for idx2 in range(idx + 1, idx + 1001):
            if has_repeating(get_hash_fn(salt, idx2), 5, c):
                keys.append(idx)
                if len(keys) == 64:
                    return idx
                break
    return None


def solve(salt):
    # part 1
    result = find_keys(salt, get_hash)
    print("Part 1:", result)
    # part 2
    result = find_keys(salt, get_hash_part2)
    print("Part 2:", result)


def main():
    # solve('abc')
    solve('zpqevtbw')


if __name__ == "__main__":
    main()
