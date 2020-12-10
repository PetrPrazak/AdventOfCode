# https://adventofcode.com/2020/day/10
from __future__ import print_function
from collections import Counter, defaultdict


def process(data):
    # part 1
    difs = [data[i] - data[i-1] for i in range(1, len(data))]
    cc = Counter(difs)
    result = cc[1] * cc[3]
    print("part 1:", result)
    # part 2
    # comb[i] == number of ways to connect from adapter i to device
    comb = defaultdict(int)
    comb[data.pop()] = 1
    for i in reversed(data):
        comb[i] = comb[i+1] + comb[i+2] + comb[i+3]
    print("part 2:", comb[0])


def load_data(fileobj):
    data = sorted(int(line.rstrip()) for line in fileobj)
    # charging outlet
    data = [0] + data
    # device (max + 3)
    data.append(data[-1] + 3)
    return data


def main(file):
    print(file)
    with open(file) as f:
        process(load_data(f))


if __name__ == "__main__":
    main("test.txt")
    main("test2.txt")
    main("input.txt")
