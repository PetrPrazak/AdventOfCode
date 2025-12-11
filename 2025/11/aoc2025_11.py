# https://adventofcode.com/2025/day/11
from pathlib import Path
import time
import networkx as nx


def count_paths(G, source, target):
    order = list(nx.topological_sort(G))
    dp = {node: 0 for node in G}
    dp[source] = 1

    for u in order:
        for v in G.successors(u):
            dp[v] += dp[u]
    return dp[target]


def part1(G):
    return count_paths(G, source="you", target="out")


def part2(G):
    acc = 0
    for path in [("svr", "fft", "dac", "out"), ("svr", "dac", "fft", "out")]:
        pscore = 1
        for s, t in zip(path, path[1:]):
            pscore *= count_paths(G, s, t)
            if pscore == 0:
                break
        acc += pscore
    return acc


def process(data, parts):
    G = nx.DiGraph(data)
    # part 1
    if 1 in parts:
        result = part1(G)
        print("part 1:", result)
    # part 2
    if 2 in parts:
        result = part2(G)
        print("part 2:", result)


def parse_line(line):
    fr, to = line.split(": ")
    return fr, to.split(" ")


def load_data(fileobj):
    return dict(parse_line(line.rstrip()) for line in fileobj.readlines())


def main(file="input.txt", parts={1, 2}):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        t1 = time.perf_counter()
        process(load_data(f), parts)
        t2 = time.perf_counter()
        print(f"Finished in {t2 - t1:.3f} s")


if __name__ == "__main__":
    main("test.txt", {1})
    main("test2.txt", {2})
    main()
