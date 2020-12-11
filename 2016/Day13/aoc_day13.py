# http://adventofcode.com/2016/day/13
from __future__ import print_function
from collections import deque
from functools import cache

WALL = '#'
FLOOR = '.'

@cache
def get_block_favorite(fav_number, x, y):
    num = x*(x+3) + 2*x*y + y*(y+1)
    num += fav_number
    suma = sum(b == '1' for b in format(num, 'b'))
    return WALL if (suma % 2) == 1 else FLOOR


directions = [(0, +1),
              (0, -1),
              (+1, 0),
              (-1, 0)]


def block_in_grid(grid, get_block, pos):
    if pos in grid:
        block = grid[pos]
    else:
        block = get_block(pos)
        grid[pos] = block
    return block


def walk_grid(get_block, source, target=None, max_dist=None):
    grid = dict()
    dist = dict()
    grid[source] = 'O'
    dist[source] = 0
    Q = deque()
    Q.append(source)
    while Q:
        x, y = Q.popleft()
        for dx, dy in directions:          # explore all directions
            newx = x + dx
            newy = y + dy
            if newx < 0 or newy < 0:
                continue                   # reached the bounds of the grid
            pos = newx, newy
            block = block_in_grid(grid, get_block, pos)
            if block != FLOOR:
                continue                   # inaccessible or already visited
            if max_dist and dist[(x, y)] >= max_dist:
                continue
            grid[pos] = 'O'                # mark visit
            if pos not in dist:
                dist[pos] = dist[(x, y)] + 1
            if pos == target:
                return dist                # goal is reached
            Q.append(pos)
    return dist


def solve(fav_number):
    # part 1
    def get_block(t): return get_block_favorite(fav_number, *t)
    dist = walk_grid(get_block, (1, 1), (31, 39))
    result = dist[(31, 39)]
    print("Part 1:", result)
    # part 2
    dist = walk_grid(get_block, (1, 1), None, 50)
    result = len(dist)
    print("Part 2:", result)


if __name__ == "__main__":
    solve(1364)
