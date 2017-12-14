from __future__ import print_function

"""
http://adventofcode.com/2016/day/4
"""

import re
from collections import Counter,defaultdict

regex = re.compile(r"([a-z-]+)-(\d+)\[([a-z]+)\]")

def solve(lines):
    sum  = 0
    for line in lines:
        r = regex.match(line)
        name = r.group(1).replace('-','')
        letters = Counter(name)
        d = defaultdict(str)
        for l in letters.keys():
            d[letters[l]] += l
        realname = "".join(["".join(sorted(d[k])) for k in sorted(d.keys(), reverse=True)])
        checksum = r.group(3)
        if realname[:5] == checksum:
            num = int(r.group(2))
            sum += num
    print(sum)

def solve2(lines):
    modul = ord('z') - ord('a') + 1
    for line in lines:
        r = regex.match(line)
        name = r.group(1).replace('-',' ')
        room = int(r.group(2))
        realname = "".join([chr(ord('a') + ((ord(c) - ord('a') + room) % modul)) if c is not ' ' else ' ' for c in list(name)])
        print(realname, room)

if __name__ == "__main__":
    # with open("day4_input_test.txt") as f:
    #     lines = f.readlines()
    #     solve2(lines)
    with open("day4_input.txt") as f:
        lines = f.readlines()
        solve2(lines)
 