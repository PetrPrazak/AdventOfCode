# https://adventofcode.com/2023/day/8
from pathlib import Path
from itertools import cycle
from math import lcm
import time


def solve(data, start_node, ending):
    directions, graph = data
    steps, next_node = 1, start_node
    for d in cycle(directions):
        part = 0 if d == 'L' else 1
        next_node = graph[next_node][part]
        if ending(next_node):
            break
        steps += 1
    return steps


def part2(data):
    _, graph = data
    start_nodes = [node for node in graph if node[-1] == 'A']
    all_steps = [solve(data, s, lambda n: n[-1] == 'Z') for s in start_nodes]
    return lcm(*all_steps)


def process(data):
    # part 1
    result = solve(data, 'AAA', lambda n: n == 'ZZZ')
    print("part 1:", result)
    # part 2
    result = part2(data)
    print("part 2:", result)


def parse_line(line):
    fr, to = line.split(" = ")
    left, right = to[1:-1].split(", ")
    return fr, (left, right)


def load_data(fileobj):
    lines = [line.rstrip() for line in fileobj.readlines()]
    directions, network = lines[0], lines[2:]
    return directions, dict(parse_line(l) for l in network)


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        t1 = time.perf_counter()
        process(load_data(f))
        t2 = time.perf_counter()
        print(f"Finished in {t2 - t1:.3f} s")


if __name__ == "__main__":
    # main("test2.txt")
    main()
