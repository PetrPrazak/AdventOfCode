# https://adventofcode.com/2025/day/10
from z3 import *
from pathlib import Path
from collections import deque
import time


def toggle_lights(lights, button):
    return tuple(not l if i in button else l for i, l in enumerate(lights))


def shortest_path(start, target, buttons):
    previous = {start: None}
    q = deque()
    q.append(start)
    while q:
        state = q.popleft()
        for button in buttons:
            next = toggle_lights(state, button)
            if next not in previous:
                previous[next] = state
                q.append(next)
    # count path length
    l, s = 0, target
    while s != start:
        s = previous[s]
        l += 1
    return l


def part1(data):
    return sum(shortest_path(tuple([False] * len(lights)), lights, buttons)
               for lights, buttons, _ in data)


def part2(data):
    acc = 0
    for _, buttons, joltage in data:
        s = Optimize()
        C = IntVector('press', len(buttons))
        for c in C:
            # don't allow negative results
            s.add(c >= 0)
        for counter, jolt in enumerate(joltage):
            s.add(Sum([C[i] for i, button in enumerate(buttons) if counter in button])
                  == jolt)
        s.minimize(Sum(C))
        assert s.check() == sat
        m = s.model()
        acc += sum(m[v].as_long() for v in m)

    return acc


def process(data):
    # part 1
    result = part1(data)
    print("part 1:", result)
    # part 2
    result = part2(data)
    print("part 2:", result)


def parse_line(line):
    lights, *buttons, joltage = line.split(' ')
    lights = tuple(c == '#' for c in lights if c in ['.', '#'])
    buttons = set(frozenset(int(b)
                  for b in bb[1:-1].split(',')) for bb in buttons)
    joltage = tuple(int(j) for j in joltage[1:-1].split(','))
    return lights, buttons, joltage


def load_data(fileobj):
    return [parse_line(line.rstrip()) for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        t1 = time.perf_counter()
        process(load_data(f))
        t2 = time.perf_counter()
        print(f"Finished in {t2 - t1:.3f} s")


if __name__ == "__main__":
    main("test.txt")
    main()
