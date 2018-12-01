"""
http://adventofcode.com/2017/day/20

"""
from __future__ import print_function
from collections import defaultdict


class Particle(object):
    __slots__ = 'p', 'v', 'a'

    def __init__(self, p, v, a):
        self.p = p
        self.a = a
        self.v = v

    def update(self):
        for i in range(3):
            self.v[i] += self.a[i]
            self.p[i] += self.v[i]

    @property
    def dist(self):
        return sum(abs(p) for p in self.p)

    def __str__(self):
        return "p={}, v = {}, a = {}".format(self.p, self.v, self.a)


# line format:
# p=<-2964,-3029,2594>, v=<-8,157,7>, a=<9,-3,-8>

def solve(lines, part=0):
    print("Part", part + 1)

    # parse lines
    particles = []
    for i, line in enumerate(lines):
        parts = line.strip().split(', ')
        data = dict()
        for p in parts:
            eq = p.split('=')
            data[eq[0]] = list(map(int, eq[1].strip('<>').split(',')))
        particles.append(Particle(data['p'], data['v'], data['a']))

    closest = None  # index of the closest particle
    change = 0  # counter how long the closest particle has not changed
    clock = 0
    while change < 1000:
        mindist = None
        curclosest = None
        positions = defaultdict(list)

        for i, particle in enumerate(particles):
            particle.update()
            dist = particle.dist
            if mindist is None or dist < mindist:
                curclosest = i
                mindist = dist

            # part 2
            # dictionary of particles keyed by position
            if part == 1:
                pos = tuple(particle.p)
                positions[pos].append(i)

        if curclosest != closest:
            closest = curclosest
            change = 0
        else:
            change += 1

        if part == 1:
            # remove particles on same positions
            todel = set()
            for v in positions.values():
                if len(v) > 1:
                    todel |= set(v)
            if todel:
                particles = [item for index, item in enumerate(particles) if index not in todel]
                if not particles:
                    break

        clock += 1

    if part == 0:
        print(closest, clock, change)
    else:
        print(len(particles))


INPUT = "aoc_day20_input.txt"
# INPUT = "aoc_day20_test.txt"


def main():
    with open(INPUT) as f:
        lines = f.readlines()
        solve(lines)
        solve(lines, 1)


if __name__ == "__main__":
    main()
