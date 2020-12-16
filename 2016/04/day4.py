# http://adventofcode.com/2016/day/4
from __future__ import print_function
import re
from collections import Counter, defaultdict


regex = re.compile(r"([a-z-]+)-(\d+)\[([a-z]+)\]")


def solve(lines):
    sum = 0
    for line in lines:
        r = regex.match(line)
        name = r.group(1).replace('-', '')
        letters = Counter(name)
        d = defaultdict(str)
        for l in letters:
            d[letters[l]] += l
        realname = "".join(["".join(sorted(d[k]))
                            for k in sorted(d.keys(), reverse=True)])
        checksum = r.group(3)
        if realname[:5] == checksum:
            num = int(r.group(2))
            sum += num
    print("Part 1:", sum)


def decrypt(char, room, modul):
    return chr(ord('a') + ((ord(char) - ord('a') + room) % modul)) if char != ' ' else ' '


def solve2(lines):
    modul = ord('z') - ord('a') + 1
    for line in lines:
        r = regex.match(line)
        name = r.group(1).replace('-', ' ')
        room = int(r.group(2))
        realname = "".join(decrypt(c, room, modul) for c in list(name))
        if realname == 'northpole object storage':
            print("Part 2:", room)
            return


def main(file):
    with open(file) as f:
        lines = f.readlines()
        solve(lines)
        solve2(lines)


if __name__ == "__main__":
    # main("day4_input_test.txt")
    main("day4_input.txt")
