# https://adventofcode.com/2020/day/7
from __future__ import print_function
import re


def contains(bags, colorbag, color):
    contents = bags[colorbag]
    if not contents:
        return False
    return True if color in contents else any(contains(bags, c, color) for c in contents)


def count_bags(bags, color):
    contents = bags[color]
    if not contents:
        return 0
    return sum((count_bags(bags, c) + 1) * val for c, val in contents.items())


def process(bags):
    my_bag = "shiny gold"
    # part 1
    result = sum(int(contains(bags, color, my_bag)) for color in bags)
    print("part 1:", result)
    # part 2
    result = count_bags(bags, my_bag)
    print("part 2:", result)


def parse_line(line):
    color, rest = line.rstrip().split(" bags contain ")
    contain = [(color, int(count))
               for count, color in re.findall(r"(\d+) ([\w ]+) bag", rest)]
    return color, contain


def load_data(fileobj):
    colors = [parse_line(line) for line in fileobj]
    bags = {color: dict(contain) for color, contain in colors}
    return bags


def main(file):
    print(file)
    with open(file) as f:
        process(load_data(f))


if __name__ == "__main__":
    main("test.txt")
    main("input.txt")
