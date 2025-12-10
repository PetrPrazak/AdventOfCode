# https://adventofcode.com/2025/day/10
from z3 import *
from pathlib import Path
from collections import deque
import time


def switch_light(light, toggle):
    if not toggle:
        return light
    return 1 if light == 0 else 0


def toggle_lights(lights, _, button):
    return tuple(switch_light(l, i in button) for i, l in enumerate(lights))


def update_jolts(joltage, target, button):
    if any(j1 > j2 for j1, j2 in zip(joltage, target)):
        return None
    return tuple((j + 1) if i in button else j for i, j in enumerate(joltage))


def shortest_path(start, target, buttons, next_state):
    previous = {start: None}
    q = deque()
    q.append(start)
    while q:
        state = q.popleft()
        for button in buttons:
            next = next_state(state, target, button)
            if next and next not in previous:
                previous[next] = state
                q.append(next)
    # count path length
    l, s = 0, target
    while s != start:
        s = previous[s]
        l += 1
    return l


def part1(data):
    return sum(shortest_path(tuple([0] * len(lights)), lights, buttons, toggle_lights)
               for lights, buttons, _ in data)


# Source - https://stackoverflow.com/a/70656700
# Posted by alias, modified by community. See post 'Timeline' for change history
# Retrieved 2025-12-10, License - CC BY-SA 4.0
def all_smt(s, initial_terms):
    def block_term(s, m, t):
        s.add(t != m.eval(t, model_completion=True))

    def fix_term(s, m, t):
        s.add(t == m.eval(t, model_completion=True))

    def all_smt_rec(terms):
        if sat == s.check():
            m = s.model()
            yield m
            for i in range(len(terms)):
                s.push()
                block_term(s, m, terms[i])
                for j in range(i):
                    fix_term(s, m, terms[j])
                yield from all_smt_rec(terms[i:])
                s.pop()
    yield from all_smt_rec(list(initial_terms))


def part2(data):
    acc = 0
    for _, buttons, joltage in data:
        s = Solver()
        C = IntVector('press', len(buttons))
        for c in C:
            # don't allow negative results
            s.add(c >= 0)
        for counter, jolt in enumerate(joltage):
            s.add(Sum([C[i] for i, button in enumerate(buttons) if counter in button])
                  == jolt)
        acc += min(sum(m[v].as_long() for v in m) for m in all_smt(s, C))
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
    lights = tuple(0 if c == '.' else 1 for c in lights if c in ['.', '#'])
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
    # main("test.txt")
    main()
