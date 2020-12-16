# http://adventofcode.com/2015/day/5
from __future__ import print_function
from collections import Counter


def is_nice(word):
    for f in ["ab", "cd", "pq", "xy"]:
        if f in word:
            return False

    c = Counter(word)
    if sum(c[v] for v in "aeiou") < 3:
        return False

    p = word[0]
    for i in range(1, len(word)):
        if p == word[i]:
            return True
        p = word[i]
    return False


def has_pair(word):
    p = word[0:2]
    for i in range(1, len(word)):
        idx = word[i + 1:].find(p)
        if idx != -1:
            return True
        p = word[i:i + 2]
    return False


def is_nice2(word):
    if not has_pair(word):
        return False

    p = word[0]
    for i in range(1, len(word) - 1):
        if p == word[i + 1]:
            return True
        p = word[i]
    return False


def main():
    with open("input.txt") as f:
        data = [l.strip() for l in f.readlines()]
        print(sum(is_nice(s) for s in data))
        print(sum(is_nice2(s) for s in data))


if __name__ == "__main__":
    main()
