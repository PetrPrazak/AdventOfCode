# http://adventofcode.com/2015/day/9
from __future__ import print_function
from collections import defaultdict


def find_path(graph, start, cities, op):
    if not cities:
        return 0, [start]
    edges = graph[start]
    nextto = op(cities, key=(lambda k: edges[k]))
    distance, stops = find_path(graph, nextto, cities - {nextto}, op)
    return edges[nextto] + distance, [start] + stops


def process(graph):
    # part 1
    cities = set(graph.keys())
    trips = [find_path(graph, k, cities-{k}, min) for k in graph.keys()]
    print("Part 1:", min(trips)[0])
    trips = [find_path(graph, k, cities-{k}, max) for k in graph.keys()]
    print("Part 2:", max(trips)[0])


def parse(line):
    start, _, end, _, length = line.split()
    return [(start, (end, int(length))), (end, (start, int(length)))]


def load_data(fileobj):
    data = [edge for line in fileobj for edge in parse(line)]
    # return data
    graph = defaultdict(dict)
    for e in data:
        start, end = e
        to, val = end
        graph[start][to] = val
    return graph


def main(file):
    print(file)
    with open(file) as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main("input.txt")
