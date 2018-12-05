# https://adventofcode.com/2018/day/5

from __future__ import print_function

INPUT = "aoc2018_day05.txt"
TEST = "dabAcCaCBAcCcaDA"

def isPair(one, two):
    if one.islower():
        return one.upper() == two
    elif two.islower():
        return one == two.upper()
    return False


def react(data):
    chain = data.copy()
    index = 0
    while(index < len(chain) - 1):
        if isPair(chain[index], chain[index + 1]):
            del chain[index:index+2]
            if index > 0:
                index -= 1
        else:
            index += 1
    return len(chain)


def process(data):
    # part 1
    print(react(data))
    # part 2
    letters = set([x.upper() for x in data])
    results = list()
    for l in letters:
        fixed = [x for x in data if x.upper() != l]
        results.append((l,react(fixed)))
    print(sorted(results, key=lambda t: t[1])[0])


with open(INPUT) as f:
    data = f.readline().rstrip()
    # process(list(TEST))
    process(list(data))
