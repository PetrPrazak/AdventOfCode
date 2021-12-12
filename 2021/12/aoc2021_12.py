# https://adventofcode.com/2021/day/12
from __future__ import print_function
from os import path
from pprint import pprint
from pathlib import Path
from functools import cache
from collections import defaultdict


def make_graph(data):
    def add_connection(graph, begin, end):
        if begin != 'end' and end != 'start':
            graph[begin].add(end)

    graph = defaultdict(set)
    for n1, n2 in data:
        add_connection(graph, n1, n2)
        add_connection(graph, n2, n1)
    return graph


@cache
def is_small(cave):
    return all(n.islower() for n in cave)


def next_node(graph, node, small_cave, all_paths, path=None):
    if path is None:
        path = []
    path.append(node)
    for n in graph[node]:
        if n == 'end':
            path.append(n)
            all_paths.append(path)
        elif not (is_small(n) and n in path) or n == small_cave and path.count(n) < 2:
            next_node(graph, n, small_cave, all_paths, path.copy())


def find_paths(graph, small_cave=None):
    paths = []
    next_node(graph, 'start', small_cave, paths)
    return paths


def process(data):
    # part 1
    graph = make_graph(data)
    result = len(find_paths(graph))
    print("part 1:", result)
    # part 2
    small_caves = {cave for cave in graph if cave != 'start' and is_small(cave)}
    all_paths = set()
    for cave in small_caves:
        all_paths.update({','.join(path) for path in find_paths(graph, cave)})
    result = len(all_paths)
    print("part 2:", result)


def parse_line(line):
    return line.strip().split("-")


def load_data(fileobj):
    return [parse_line(line) for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
