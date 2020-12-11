# https://adventofcode.com/2020/day/6
from __future__ import print_function


def count_answers(group):
    answers = set.union(*map(set, group))
    return len(answers)


def count_all_answers(group):
    answers = set.intersection(*map(set, group))
    return len(answers)


def process(data):
    # part 1
    result = sum(count_answers(group.split()) for group in data)
    print("Part 1:", result)

    # part 2
    result = sum(count_all_answers(group.split()) for group in data)
    print("Part 2:", result)


def load_data(fileobj):
    return fileobj.read().split('\n\n')


def main(file):
    print(file)
    with open(file) as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main("input.txt")
