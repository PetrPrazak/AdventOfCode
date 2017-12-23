"""
http://adventofcode.com/2015/day/5
"""
from __future__ import print_function
from collections import Counter


def is_nice(word):
    for f in ["ab", "cd", "pq", "xy"]:
        idx = word.find(f)
        if idx != -1:
            return False

    c = Counter(word)
    l = [c[v] for v in list("aeiou")]
    if sum(l) < 3:
        return False

    p = word[0]
    for i in range(1, len(word)):
        if p == word[i]:
            break
        p = word[i]
    else:
        i = len(word)

    return i < len(word)


def is_nice2(word):
    p = word[0:2]
    for i in range(1, len(word)):
        idx = word[i + 1:].find(p)
        if idx != -1:
            break
        p = word[i:i + 2]
    else:
        i = len(word)
    c = i < len(word)
    if not c:
        return False

    p = word[0]
    for i in range(1, len(word) - 1):
        if p == word[i + 1]:
            break
        p = word[i]
    else:
        i = len(word) - 1

    return i < len(word) - 1


def main():
    with open("input.txt") as f:
        data = [l.strip() for l in f.readlines()]
        print(sum(is_nice(s) for s in data))
        print(sum(is_nice2(s) for s in data))


if __name__ == "__main__":
    main()
