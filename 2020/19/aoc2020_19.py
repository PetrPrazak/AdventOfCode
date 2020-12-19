# https://adventofcode.com/2020/day/19
from __future__ import print_function
import re


def reduce_rules(rules, term="0"):
    right = rules[term]
    if type(right) is list:
        out = []
        for part in right:
            right_rules = (reduce_rules(rules, t) for t in part)
            out.append(''.join(right_rules))
        return '(?:' + '|'.join(out) + ')' if len(out) > 1 else out[0]
    else:
        return right


def count_matching(rules, lines):
    reg = reduce_rules(rules)
    return sum(bool(re.fullmatch(reg, line)) for line in lines)


def part1(data):
    rules, data = data
    return count_matching(rules, data)


def part2(data):
    # part 2
    rules, data = data
    rules["8"] = [['42', 'P']]
    rules["P"] = "+"
    # 11: 42{1}31{1} | ... | 42{x}31{x}
    rule11 = [['42', '31']]
    for i in range(2, 6):  # upper limit found experimentally
        term = f"R{i}"
        rule11.append(['42', term, '31', term])
        rules[term] = f"{{{i}}}"
    rules["11"] = rule11
    return count_matching(rules, data)


def process(data):
    # part 1
    print("part 1:", part1(data))
    print("part 2:", part2(data))


def parse_rule(rule):
    term, right = rule.split(": ")
    if right[0] == '"':
        target = right.strip('"')
    else:
        target = [list(part.split(" ")) for part in right.split(" | ")]
    return term, target


def parse_rules(rules):
    return dict(parse_rule(rule) for rule in rules.split("\n"))


def load_data(fileobj):
    rules, data = fileobj.read().split("\n\n")
    return parse_rules(rules), [l for l in data.split()]


def main(file):
    print(file)
    with open(file) as f:
        process(load_data(f))


if __name__ == "__main__":
    main("test.txt")
    main("input.txt")
