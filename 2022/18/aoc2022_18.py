# https://adventofcode.com/2022/day/18
from pathlib import Path
from operator import itemgetter
from collections import deque
import time


def get_surfaces(x, y, z):
    return {
        'x': {(x-1, y, z), (x, y, z)},
        'y': {(x, y-1, z), (x, y, z)},
        'z': {(x, y, z-1), (x, y, z)}
    }


def get_adjacent(x, y, z):
    return (
        (x-1, y, z), (x+1, y, z),
        (x, y-1, z), (x, y+1, z),
        (x, y, z-1), (x, y, z+1)
    )


def unique_surfaces(surfaces, cubes):
    for cube_surface in (get_surfaces(*c) for c in cubes):
        for axis, surface in surfaces.items():
            surfaces[axis] = surface.symmetric_difference(cube_surface[axis])


def fill_steam(cubes):
    space_min = tuple(min(cubes, key=itemgetter(i))[i]-1 for i in range(3))
    space_max = tuple(max(cubes, key=itemgetter(i))[i]+1 for i in range(3))
    grid = set((x, y, z)
               for x in range(space_min[0], space_max[0] + 1)
               for y in range(space_min[1], space_max[1] + 1)
               for z in range(space_min[2], space_max[2] + 1))
    cubes_set = set(cubes)
    visited = set()
    queue = deque([space_min])
    while queue:
        voxel = queue.popleft()
        if voxel in visited:
            continue
        visited.add(voxel)
        for adj in get_adjacent(*voxel):
            if adj in grid and adj not in visited and adj not in cubes_set:
                queue.append(adj)

    unreachable = grid.difference(visited).difference(cubes_set)
    return unreachable


def process(data):
    # part 1
    surfaces = {axis: set() for axis in 'xyz'}
    unique_surfaces(surfaces, data)
    result = sum(len(s) for s in surfaces.values())
    print("part 1:", result)
    # part 2
    unreachable = fill_steam(data)
    unique_surfaces(surfaces, unreachable)
    result = sum(len(s) for s in surfaces.values())
    print("part 2:", result)


def parse_line(line):
    return tuple(map(int, line.split(',')))


def load_data(fileobj):
    return [parse_line(line.rstrip()) for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        t1 = time.perf_counter()
        process(load_data(f))
        t2 = time.perf_counter()
        print(f"Finished in {t2 - t1:.3} s")


if __name__ == "__main__":
    # main("test.txt")
    main()
