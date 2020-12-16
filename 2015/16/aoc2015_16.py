# http://adventofcode.com/2015/day/16
from __future__ import print_function
from collections import defaultdict

ticker = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1
}


def match_aunt(aunt, props):
    return all(prop not in aunt or count == aunt[prop] for prop, count in props.items())


def is_real_aunt(prop, prop_count, count):
    return (prop in ['cats', 'trees'] and count < prop_count) \
        or (prop in ['pomeranians', 'goldfish'] and count > prop_count) \
        or count == prop_count


def match_real_aunt(aunt, props):
    return all(prop not in aunt or is_real_aunt(prop, aunt[prop], count)
               for prop, count in props.items())


def process(data):
    # part 1
    result = [aunt for aunt in data if match_aunt(data[aunt], ticker)]
    print("Part 1:", result[0])
    # part 2
    result = [aunt for aunt in data if match_real_aunt(data[aunt], ticker)]
    print("Part 2:", result[0])


def parse_prop(prop):
    prop_name, value = prop.split(': ')
    return prop_name, int(value)


def parse(line):
    sep = line.find(':')
    name = int(line[:sep].split()[1])
    props = line[sep+2:].split(', ')
    line = [parse_prop(prop) for prop in props]
    return name, line


def load_data(fileobj):
    data = [parse(line.strip()) for line in fileobj]
    aunts = {name: dict(props) for name, props in data}
    return aunts


def main(file):
    print(file)
    with open(file) as f:
        process(load_data(f))


if __name__ == "__main__":
    main("input.txt")
