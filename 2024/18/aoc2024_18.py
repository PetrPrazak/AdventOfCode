# https://adventofcode.com/2024/day/18
from pathlib import Path
from heapq import heappop, heappush
from math import inf as INFINITY
import time


def dijkstra(start, target, moves_f):
    path_cost = {start: 0}  # The cost of the best path to a state.
    pq = [(0, start)]
    while pq:
        total, current = heappop(pq)
        if current == target:
            return total
        for neighbor in moves_f(current):
            new_cost = path_cost[current] + 1
            if new_cost < path_cost.get(neighbor, INFINITY):
                heappush(pq, (new_cost, neighbor))
                path_cost[neighbor] = new_cost
    return None


def path_len(grid, width, start, end):
    def moves(pos):
        for off_x, off_y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x, y = pos[0] + off_x, pos[1] + off_y
            if 0 <= x < width and 0 <= y < width and (x, y) not in grid:
                yield x, y
    return dijkstra(start, end, moves)


def check_grid_path(data, width, cutoff):
    grid = set(data[:cutoff])
    return path_len(grid, width, (0, 0), (width-1, width-1))


def process(data, width, cutoff=1024):
    # part 1
    result = check_grid_path(data, width, cutoff)
    print("part 1:", result)
    # part 2
    low, top = cutoff, len(data)
    while low < top:
        mid = low + (top - low) // 2
        if check_grid_path(data, width, mid):
            low = mid + 1
        else:
            top = mid - 1
    pos = data[low]
    print(f"part 2: {pos[0]},{pos[1]}")


def parse_line(line):
    return tuple(map(int, line.split(",")))


def load_data(fileobj):
    return [parse_line(line.rstrip()) for line in fileobj.readlines()]


def main(file="input.txt", width=71, cutoff=1024):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        t1 = time.perf_counter()
        process(load_data(f), width, cutoff)
        t2 = time.perf_counter()
        print(f"Finished in {t2 - t1:.3f} s")


if __name__ == "__main__":
    # main("test.txt", 7, 12)
    main()
