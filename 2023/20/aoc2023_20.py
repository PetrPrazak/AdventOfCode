# https://adventofcode.com/2023/day/20
from pathlib import Path
from collections import deque
from math import lcm
import time


def propagate(graph, flops, conjs, sender, receiver, pulse):
    if receiver in flops:
        if pulse:
            return
        next_pulse = not flops[receiver]
        flops[receiver] = next_pulse
    elif receiver in conjs:
        conjs[receiver][sender] = pulse
        next_pulse = not all(conjs[receiver].values())
    elif receiver in graph:
        next_pulse = pulse
    else:
        return

    for new_receiver in graph[receiver]:
        yield (receiver, new_receiver, next_pulse)


def run(graph, flops, conjs):
    q = deque([('button', 'broadcaster', False)])
    highs = lows = 0
    while q:
        sender, receiver, pulse = q.popleft()
        if pulse:
            highs += 1
        else:
            lows += 1
        q.extend(propagate(graph, flops, conjs, sender, receiver, pulse))
    return highs, lows


def find_periods(graph, flops, conjs):
    periodic = set()
    for rx_source, receivers in graph.items():
        if 'rx' in receivers:
            break
    for source, receivers in graph.items():
        if rx_source in receivers:
            periodic.add(source)

    iteration = 1
    while True:
        q = deque([('button', 'broadcaster', False)])
        while q:
            sender, receiver, pulse = q.popleft()
            if not pulse and receiver in periodic:
                yield iteration
                periodic.remove(receiver)
                if not periodic:
                    return
            q.extend(propagate(graph, flops, conjs, sender, receiver, pulse))
        iteration += 1


def process(data):
    # part 1
    graph, flops, conjs = data
    total_highs = total_lows = 0
    for _ in range(1000):
        hi, lo = run(graph, flops, conjs)
        total_highs += hi
        total_lows += lo
    result = total_highs * total_lows
    print("part 1:", result)
    # part 2
    for f in flops:
        flops[f] = False
    for inputs in conjs.values():
        for i in inputs:
            inputs[i] = False

    result = lcm(*find_periods(graph, flops, conjs))
    print("part 2:", result)


def parse_line(line):
    fro, to = line.split(' -> ')
    typ = None
    if fro.startswith('%') or fro.startswith('&'):
        typ = fro[0]
        fro = fro[1:]
    return fro, (typ, to.split(', '))


def process_graph(data):
    flops = dict()
    conjs = dict()
    for node in data:
        typ, dest = data[node]
        if typ == '%':
            flops[node] = False
        elif typ == '&':
            conjs[node] = {}
        data[node] = dest

    for source, dests in data.items():
        for dest in filter(conjs.__contains__, dests):
            conjs[dest][source] = False

    return data, flops, conjs


def load_data(fileobj):
    return process_graph(dict(parse_line(line.rstrip()) for line in fileobj.readlines()))


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
