# https://adventofcode.com/2023/day/19
from pathlib import Path
from operator import lt, gt
from collections import deque
from copy import deepcopy
from math import prod
import time


def eval_rules(rules, rating):
    OPS = {'<': lt, '>': gt}
    node = 'in'
    while True:
        workflow = rules[node]
        for r in workflow:
            if ':' in r:
                cond, next_node = r.split(':')
                var, op = cond[0], cond[1]
                val = int(cond[2:])
                if not OPS[op](rating[var], val):
                    continue
            else:
                next_node = r
            if next_node == 'A':
                return True
            elif next_node == 'R':
                return False
            else:
                node = next_node
                break


def part2(rules):
    ranges = {'x': (1, 4000), 'm': (1, 4000), 'a': (1, 4000), 's': (1, 4000)}
    q = deque([('in', 0, ranges)])
    total = 0
    while q:
        node, idx, rating = q.popleft()
        rule = rules[node]
        rule_part = rule[idx]
        if ':' in rule_part:
            cond, next_node = rule_part.split(':')
            var, op, val = cond[0], cond[1], int(cond[2:])
            low, high = rating[var]
            if op == '<':
                if high >= val:
                    rating2 = deepcopy(rating)
                    rating2[var] = val, high
                    q.append((node, idx + 1, rating2))
                if low < val - 1:
                    rating[var] = low, val - 1
                else:
                    continue
            elif op == '>':
                if low <= val:
                    rating2 = deepcopy(rating)
                    rating2[var] = low, val
                    q.append((node, idx + 1, rating2))
                if high > val + 1:
                    rating[var] = val + 1, high
                else:
                    continue
            else:
                raise ValueError(f"unknown operator {op}")
        else:
            next_node = rule_part

        if next_node == 'A':
            total += prod(b + 1 - a for a, b in rating.values())
        elif next_node == 'R':
            continue
        else:
            q.append((next_node, 0, rating))

    return total


def process(data):
    # part 1
    rules, ratings = data
    result = sum(sum(r.values()) for r in ratings if eval_rules(rules, r))
    print("part 1:", result)
    # part 2
    result = part2(rules)
    print("part 2:", result)


def parse_rule(rule):
    name, definition = rule.split("{")
    return name, definition[:-1].split(',')


def parse_data(data):
    d = dict()
    for part in data.strip('{}').split(','):
        k, v = part.split('=')
        d[k] = int(v)
    return d


def load_data(fileobj):
    rules, data = fileobj.read().split("\n\n")
    return dict(map(parse_rule, rules.split('\n'))), list(map(parse_data, data.split("\n")))


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        t1 = time.perf_counter()
        process(load_data(f))
        t2 = time.perf_counter()
        print(f"Finished in {t2 - t1:.3f} s")


if __name__ == "__main__":
    # main("test.txt")
    main()
