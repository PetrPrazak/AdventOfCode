from __future__ import print_function
from collections import Counter, defaultdict


def find_abba(word):
    for p in range(len(word)-3):
        abba = word[p:p+4]
        # print(abba)
        if abba[0] == abba[3] and abba[1] == abba[2] and abba[0] != abba[1]:
            return abba
    return None

# import re
#
# REGEX = re.compile(r'([a-z]+)(\[([a-z]+)\]([a-z]+))+')

def check_parts(parts):
    has_abba = False
    for part in parts:
        if len(part) > 1:
            if find_abba(part[1]):
                return False
        if not has_abba:
            has_abba = find_abba(part[0])
    return has_abba


def solve(lines):
    sum = 0
    for line in lines:
        parts = [w.split('[') for w in line.strip().split(']')]
        if check_parts(parts):
            sum += 1
    print(sum)


def get_abas(word):
    abas = []
    for p in range(len(word)-2):
        a = word[p:p+3]
        if a[0] == a[2] and a[0] != a[1]:
            abas.append(a)
    return abas


def check_parts2(parts, line):

    for part in parts:
        abas = get_abas(part[0])
        # print(abas)
        for aba in abas:
            bab = aba[1] + aba[0] + aba[1]
            if line.find(bab) != -1:
                print(line,aba,bab)
                return True
    return False


def solve2(lines):
    sum = 0
    for line in lines:
        line = line.strip()
        parts = [w.split('[') for w in line.split(']')]
        if check_parts2(parts, line):

            sum += 1
        # break
    print(sum)

# INPUT = "aoc_day7_test.txt"
INPUT = "aoc_day7_input.txt"

if __name__ == "__main__":
    with open(INPUT) as f:
       l = f.readlines()
    solve2(l)
