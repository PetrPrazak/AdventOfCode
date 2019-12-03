# https://adventofcode.com/2019/day/03

from __future__ import print_function

INPUT = "aoc2019_03_input.txt"


# 2-D points implemented using (x, y) tuples
def X(point): return point[0]


def Y(point): return point[1]


def cityblock_distance(p, q=(0, 0)):
    """City block distance between two points."""
    return abs(X(p) - X(q)) + abs(Y(p) - Y(q))


# returns the list of wire positions so we can find the length of wire to each point
def compute_points(wire):
    path = list()
    pos = 0, 0
    for step in wire.split(","):
        direction = step[0]
        stride = int(step[1:])
        for _ in range(stride):
            if direction == "R":
                pos = X(pos) + 1, Y(pos)
            elif direction == "L":
                pos = X(pos) - 1, Y(pos)
            elif direction == "U":
                pos = X(pos), Y(pos) + 1
            elif direction == "D":
                pos = X(pos), Y(pos) - 1
            else:
                assert False, "Wrong direction %r" % direction
            path.append(pos)
    return path


# return the list of crossings and sum of wire lengths to each crossing
def get_itersections(wire_list):
    grid = set()
    intersections = set()
    wire_paths = [compute_points(wire) for wire in wire_list]
    for path in wire_paths:
        points = set(path)
        intersections.update(grid.intersection(points))
        grid.update(points)

    res = [(cityblock_distance(xing), sum([path.index(xing) + 1 for path in wire_paths])) for xing in intersections]
    return res


# finds the closest intersection of wires (part 1)
# and smallest length of wire to an intersection (part 2)
def get_closest_itersection(wire_list):
    intersections = get_itersections(wire_list)
    return min(intersections)[0], min(intersections, key=lambda x: x[1])[1]


def test():
    # (6, 30)
    print(get_closest_itersection(["R8,U5,L5,D3", "U7,R6,D4,L4"]))
    # (159, 610)
    print(get_closest_itersection(["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"]))
    # (135, 410)
    print(get_closest_itersection(
        ["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"]))


def process(data):
    res = get_closest_itersection(data)
    # part 1
    print(res[0])
    # part 2
    print(res[1])


def main():
    with open(INPUT) as f:
        data = [l.strip() for l in f.readlines()]
        process(data)


if __name__ == "__main__":
    # test()
    main()
