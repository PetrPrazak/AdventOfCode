# http://adventofcode.com/2015/day/3
from __future__ import print_function


def walk(visits, data, start):
    x, y = 0, 0
    for i in range(start, len(data), 2):
        direction = data[i]
        if direction == '^':
            y -= 1
        elif direction == '<':
            x -= 1
        elif direction == '>':
            x += 1
        elif direction == 'v':
            y += 1
        visits.add((x, y))


def main():
    with open("input.txt") as f:
        data = f.read().strip()

        visits = {(0, 0)}
        walk(visits, data, 0)
        walk(visits, data, 1)

        print(len(visits))


if __name__ == "__main__":
    main()
