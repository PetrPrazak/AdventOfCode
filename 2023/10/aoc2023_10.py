# https://adventofcode.com/2023/day/10
from pathlib import Path
from collections import deque
import time

UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)

LEADS = {
    UP: ['|', 'F', '7'],
    DOWN: ['|', 'L', 'J'],
    LEFT: ['-', 'L', 'F'],
    RIGHT: ['-', '7', 'J']
}

PIPES = {
    'F': [RIGHT, DOWN],
    '7': [LEFT, DOWN],
    'L': [RIGHT, UP],
    'J': [LEFT, UP],
    '|': [UP, DOWN],
    '-': [LEFT, RIGHT],
    'S': [UP, DOWN, LEFT, RIGHT]
}


def neighbors(grid, pos):
    x, y = pos
    rows, cols = len(grid), len(grid[0])
    cell = grid[x][y]
    for dir in PIPES[cell]:
        dx, dy = dir
        xx, yy = x + dx, y + dy
        if 0 <= xx < rows and 0 <= yy < cols \
                and grid[xx][yy] in LEADS[dir]:
            yield xx, yy


def start_pos(data):
    for r, l in enumerate(data):
        for c, x in enumerate(l):
            if x == 'S':
                return r, c


def walk_pipes(data):
    start = start_pos(data)
    visited = {start: 0}
    q = deque([(0, start)])
    while q:
        dist, pos = q.popleft()
        if pos == start and dist > 0:
            break
        dist += 1
        for n in neighbors(data, pos):
            if visited.get(n, float('inf')) > dist:
                q.append((dist, n))
                visited[n] = dist

    return visited


def scan_grid(data, visited):
    insides = 0
    for r, l in enumerate(data):
        is_inside = False
        for c, cell in enumerate(l):
            if cell in ['F', '7', '|', 'S'] and (r, c) in visited:
                is_inside = not is_inside
            if is_inside and (r, c) not in visited:
                insides += 1
    return insides


def process(data):
    # part 1
    visited = walk_pipes(data)
    result = max(visited.values())
    print("part 1:", result)
    # part 2
    result = scan_grid(data, visited)
    print("part 2:", result)


def load_data(fileobj):
    return [list(line.rstrip()) for line in fileobj.readlines()]


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
