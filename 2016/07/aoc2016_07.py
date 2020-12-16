# http://adventofcode.com/2016/day/7
from __future__ import print_function


def find_abba(word):
    for p in range(len(word) - 3):
        abba = word[p:p + 4]
        if abba[0] == abba[3] and abba[1] == abba[2] and abba[0] != abba[1]:
            return abba
    return None


def check_parts(parts):
    has_abba = False
    for part in parts:
        if len(part) > 1:
            if find_abba(part[1]):
                return False
        if not has_abba:
            has_abba = find_abba(part[0])
    return has_abba


def solve1(lines):
    suma = 0
    for line in lines:
        parts = [w.split('[') for w in line.strip().split(']')]
        if check_parts(parts):
            suma += 1
    print("Part 1:", suma)


def abas(word):
    for p in range(len(word) - 2):
        a = word[p:p + 3]
        if a[0] == a[2] and a[0] != a[1]:
            yield a


def check_parts2(supernets, hypernets, line):
    for part in supernets:
        for aba in abas(part):
            bab = aba[1] + aba[0] + aba[1]
            for h in hypernets:
                if h.find(bab) != -1:
                    return True
    return False


def solve2(lines):
    suma = 0
    for line in lines:
        line = line.strip()
        parts = [w.split('[') for w in line.split(']')]
        supernets = [p[0] for p in parts]
        hypernets = [p[1] for p in parts if len(p) > 1]
        if check_parts2(supernets, hypernets, line):
            suma += 1
    print("Part 2:", suma)


def main(file):
    with open(file) as f:
        l = f.readlines()
    solve1(l)
    solve2(l)


if __name__ == "__main__":
    # main("test.txt")
    main("input.txt")
