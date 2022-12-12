# https://adventofcode.com/2022/day/12
from pathlib import Path
from heapq import heappush, heappop
from math import inf as INFINITY


def neighbors4(point):
    """The four neighbors (without diagonals)."""
    x, y = point
    return (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)


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


def shortest_path(grid, start, target):

    def move(pos):
        elevation = grid[pos]
        for new_pos in neighbors4(pos):
            if (new_elevation := grid.get(new_pos)) is not None:
                if elevation - new_elevation <= 1:
                    yield new_pos

    return dijkstra(start, target, move)


def elevation(x):
    return ord(x) - ord('a')


def find_start_target(grid):
    start = target = None
    S, E = elevation('S'), elevation('E')
    for pos, val in grid.items():
        if val == S:
            start = pos
        if val == E:
            target = pos
        if start and target:
            break
    return start, target


def process(grid):
    # part 1
    start, target = find_start_target(grid)
    grid[start] = elevation('a')
    grid[target] = elevation('z')
    result = shortest_path(grid, target, start)
    print("part 1:", result)
    # part 2
    # all 'a' fields with 'b' as a neighbor
    starts = [pos for pos, val in grid.items()
              if val == 0 and any(grid.get(npos) == 1 for npos in neighbors4(pos))]
    result = min(shortest_path(grid, target, start)
                 for start in starts)
    print("part 2:", result)


def load_data(fileobj):
    grid = dict(((x, y), elevation(letter))
                for y, line in enumerate(fileobj)
                for x, letter in enumerate(line.rstrip()))
    return grid


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()

# nice solution from Reddit:
# https://topaz.github.io/paste/#XQAAAQCMAQAAAAAAAAA0m0pnuFI8c+qagMoNTEcTIfyUxhN40PtE7+ePXta4jIFIF0CejnfWaLVUZ/YTfMVYoXnegwxrKeLiuusaAR8fc1Z8zdXTdR3ADemJIwYXjPdS+NHZLg510cjUUwPX80JS+GTkrptn9gpqIqCtVmgy/VexGEhbi1e8681Z6gMv2wks1fwWeJk9baqZNjAhDoGo41CUWVyU4VQkan3PaghS/GoM56GFDKIzdm2Msxyn3Q1P5nhE1dVh86jU6F/zgCY4/A9pzE7253MJBW7OGh179/lk9nq+SPU4o5skVXybZDFwJ55QAjIFBv/O6twyHI2sgOprPcoQOqEwhtuJqwXMiQjH86PbLX0iULt4AEixvOlX3LsAl5/u++C4/fcU3g==
