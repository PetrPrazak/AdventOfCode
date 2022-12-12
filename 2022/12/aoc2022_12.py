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


def shortest_path(grid, start, target, height, width):

    def move(pos):
        max_elevation = grid[pos] + 1
        for x, y in neighbors4(pos):
            if 0 <= x < width and 0 <= y < height:
                new_elevation = grid[(x, y)]
                if new_elevation <= max_elevation:
                    yield x, y

    return dijkstra(start, target, move)


def elevation(x):
    return ord(x) - ord('a')


def find_start_target(grid):
    start = target = None
    for pos, val in grid.items():
        if val == elevation('S'):
            start = pos
        if val == elevation('E'):
            target = pos
        if start and target:
            break
    return start, target


def process(data):
    # part 1
    height, width = len(data), len(data[0])
    grid = dict(((x, y), elevation(letter))
                for y, line in enumerate(data)
                for x, letter in enumerate(line))
    start, target = find_start_target(grid)
    grid[start] = elevation('a')
    grid[target] = elevation('z')
    result = shortest_path(grid, start, target, height, width)
    print("part 1:", result)
    # part 2
    # all 'a' fields with 'b' as a neighbor
    starts = [pos for pos, val in grid.items()
              if val == 0 and any(grid.get(npos) == 1 for npos in neighbors4(pos))]
    result = min(shortest_path(grid, start, target, height, width)
                 for start in starts)
    print("part 2:", result)


def load_data(fileobj):
    return [list(line.rstrip()) for line in fileobj.readlines()]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()

# nice solution from Reddit:
# https://topaz.github.io/paste/#XQAAAQCMAQAAAAAAAAA0m0pnuFI8c+qagMoNTEcTIfyUxhN40PtE7+ePXta4jIFIF0CejnfWaLVUZ/YTfMVYoXnegwxrKeLiuusaAR8fc1Z8zdXTdR3ADemJIwYXjPdS+NHZLg510cjUUwPX80JS+GTkrptn9gpqIqCtVmgy/VexGEhbi1e8681Z6gMv2wks1fwWeJk9baqZNjAhDoGo41CUWVyU4VQkan3PaghS/GoM56GFDKIzdm2Msxyn3Q1P5nhE1dVh86jU6F/zgCY4/A9pzE7253MJBW7OGh179/lk9nq+SPU4o5skVXybZDFwJ55QAjIFBv/O6twyHI2sgOprPcoQOqEwhtuJqwXMiQjH86PbLX0iULt4AEixvOlX3LsAl5/u++C4/fcU3g==