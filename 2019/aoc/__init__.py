# https://adventofcode.com/2019/
# Common functions and classes useful for AoC

from __future__ import print_function
import re
import math
from collections import Counter, defaultdict, namedtuple, deque
from itertools import permutations, combinations, chain, cycle, product, islice
import time
from functools import wraps
from heapq import heappop, heappush

def transpose(matrix): return zip(*matrix)


def first(iterable): return next(iter(iterable))


def nth(iterable, n, default=None):
    """Returns the nth item of iterable, or a default value"""
    return next(islice(iterable, n, None), default)


cat = ''.join

Ø = frozenset()  # Empty set
inf = float('inf')
BIG = 10 ** 999


def grep(pattern, lines):
    """Print lines that match pattern."""
    for line in lines:
        if re.search(pattern, line):
            print(line)


def groupby(iterable, key=lambda it: it):
    """Return a dic whose keys are key(it) and whose values are all the elements of iterable with that key."""
    dic = defaultdict(list)
    for it in iterable:
        dic[key(it)].append(it)
    return dic


def powerset(iterable):
    """Yield all subsets of items."""
    items = list(iterable)
    for r in range(len(items) + 1):
        for c in combinations(items, r):
            yield c


# 2-D points implemented using (x, y) tuples
def X(point): return point[0]


def Y(point): return point[1]


def neighbors4(point):
    """The four neighbors (without diagonals)."""
    x, y = point
    return (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)


def neighbors8(point):
    """The eight neighbors (with diagonals)."""
    x, y = point
    return ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1),
            (X + 1, y + 1), (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1))


def cityblock_distance(p, q=(0, 0)):
    """City block distance between two points."""
    return abs(X(p) - X(q)) + abs(Y(p) - Y(q))


def euclidean_distance(p, q=(0, 0)):
    """Euclidean (hypotenuse) distance between two points."""
    return math.hypot(X(p) - X(q), Y(p) - Y(q))


def trace1(f):
    """Print a trace of the input and output of a function on one line."""
    def traced_f(*args):
        result = f(*args)
        print('{}({}) = {}'.format(f.__name__, ', '.join(map(str, args)), result))
        return result

    return traced_f


# https://en.wikipedia.org/wiki/A*_search_algorithm
def astar_search(start, h_func, moves_func):
    """Find a shortest sequence of states from start to a goal state (a state s with h_func(s) == 0)."""
    frontier = [(h_func(start), start)]  # A priority queue, ordered by path length, f = g + h
    previous = {start: None}  # start state has no previous state; other states will
    path_cost = {start: 0}  # The cost of the best path to a state.
    while frontier:
        (f, s) = heappop(frontier)
        if h_func(s) == 0:
            return Path(previous, s)
        for s2 in moves_func(s):
            new_cost = path_cost[s] + 1
            if s2 not in path_cost or new_cost < path_cost[s2]:
                heappush(frontier, (new_cost + h_func(s2), s2))
                path_cost[s2] = new_cost
                previous[s2] = s
    return dict(fail=True, front=len(frontier), prev=len(previous))


def Path(previous, s):
    """Return a list of states that lead to state s, according to the previous dict."""
    return [] if (s is None) else Path(previous, previous[s]) + [s]


# Code by Eryk Kopczyński
def find_shortest_path(graph, start, end):
    dist = {start: [start]}
    q = deque(start)
    while len(q):
        at = q.popleft()
        for next in graph[at]:
            if next not in dist:
                dist[next] = [dist[at], next]
                q.append(next)
    return dist.get(end)


def minmax_tuples(tuple_list, element=0):
    res = sorted(tuple_list, key=lambda k: k[element])
    return res[0][element], res[-1][element]


def render_grid(grid):
    coords = list(grid.keys())
    min_x, max_x = minmax_tuples(coords, 0)
    min_y, max_y = minmax_tuples(coords, 1)
    out = ""
    for line in range(min_y, max_y + 1):
        for col in range(min_x, max_x + 1):
            out += grid.get((col, line), ' ')
        out += '\n'
    return out


def print_grid(grid):
    print(render_grid(grid))


def read_input_line(filename):
    with open(filename) as f:
        data = f.readline().rstrip()
        return data


def read_input_ints(filename):
    ints = list(map(int, read_input_line(filename)))
    return ints


def read_input_ints_separated(filename, sep=','):
    ints = list(map(int, read_input_line(filename).split(sep)))
    return ints


def read_input_lines(filename):
    with open(filename) as f:
        data = [l.rstrip() for l in f.readlines()]
        return data


def read_input_lines_separated(filename, sep=','):
    return [l.split(sep) for l in read_input_lines(filename)]


def read_input_int_lines(filename):
    return list(map(int, read_input_lines(filename)))


def timeit(method):
    @wraps(method)
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('%r %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result

    return timed


if __name__ == "__main__":
    pass
