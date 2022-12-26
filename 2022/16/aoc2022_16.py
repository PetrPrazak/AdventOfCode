# https://adventofcode.com/2022/day/16
from pathlib import Path
from itertools import combinations
import time
import re
import networkx as nx


class Tunnels:
    def __init__(self, data) -> None:
        self.graph = nx.Graph()
        self.graph.add_nodes_from(data)
        for node, (valve, neighbors) in data.items():
            self.graph.nodes[node]["valve"] = valve
            for n in neighbors:
                if n in self.graph.nodes():
                    self.graph.add_edge(node, n, weight=1)
        self.shortest_paths = nx.floyd_warshall(self.graph)

    def nodes_to_visit(self):
        return set(n for n in self.graph.nodes() if self.graph.nodes[n]["valve"] > 0)

    def search_path(self, remaining, max_turns=30):
        paths = []
        self._search_path("AA", remaining, path=[], max_turns=max_turns, paths=paths)
        return paths

    def _search_path(
        self,
        start,
        remaining,
        tick=0,
        rate=0,
        flow=0,
        path=None,
        max_turns=30,
        paths=None,
    ):
        if not remaining:
            flow += (max_turns - tick) * rate
            paths.append((path, flow))
            return flow

        for node in remaining:
            new_tick = self.shortest_paths[start][node] + 1
            if new_tick == 1 or tick + new_tick > max_turns:
                new_flow = (max_turns - tick) * rate
                paths.append((path, flow + new_flow))
                continue
            new_flow = new_tick * rate
            node_rate = self.graph.nodes[node]["valve"]
            self._search_path(
                node,
                remaining - {node},
                tick=tick + new_tick,
                rate=rate + node_rate,
                flow=flow + new_flow,
                path=path + [node],
                max_turns=max_turns,
                paths=paths,
            )


def best_flow(paths):
    return max(paths, key=lambda t: t[1])[1]


def process(data):
    # part 1
    tunnels = Tunnels(data)
    nodes = tunnels.nodes_to_visit()
    paths = tunnels.search_path(nodes)
    result = best_flow(paths)
    print("part 1:", result)
    # part 2
    max_flow = 0
    for i in range(tunnels.graph.number_of_nodes()):
        for c in combinations(nodes, i):
            s1 = set(c)
            s2 = nodes - s1
            paths = tunnels.search_path(s1, max_turns=26)
            b1 = best_flow(paths)
            paths = tunnels.search_path(s2, max_turns=26)
            b2 = best_flow(paths)
            max_flow = max(max_flow, b1 + b2)
    result = max_flow
    print("part 2:", result)


def parse_line(line):
    m = re.match(
        "Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)", line
    )
    return m.group(1), (int(m.group(2)), list(m.group(3).split(", ")))


def load_data(fileobj):
    return dict(parse_line(line.rstrip()) for line in fileobj.readlines())


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
