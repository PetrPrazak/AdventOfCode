# https://adventofcode.com/2020/day/20
from __future__ import print_function
from functools import reduce
from operator import mul
from collections import Counter, defaultdict, deque
from pprint import pprint
import re
import pathlib
import typing
import itertools
from math import floor, sqrt
from functools import cache



def transpose(matrix):
    return zip(*matrix)


def rotate_tile(tile):
    return [''.join(reversed(r)) for r in transpose(tile)]


def flip_tile(tile):
    return [''.join(reversed(l)) for l in tile]


def edge(row):
    return int(''.join('1' if p == '#' else '0' for p in row), 2)


def edges(tile):
    top = edge(tile[0])
    down = edge(tile[-1])
    rotated = rotate_tile(tile)
    left = edge(rotated[0])
    right = edge(rotated[-1])
    return [top, right, down, left]


def rotate_tiles(tiles):
    all_tiles = dict()
    all_edges = dict()
    for id, tile in tiles.items():
        variants = [tile]
        for _ in range(3):
            tile = rotate_tile(tile)
            variants.append(tile)
        variants.extend([flip_tile(tile) for tile in variants])
        all_edges[id] = [edges(tile) for tile in variants]
        all_tiles[id] = variants
    return all_edges, all_tiles


def get_rows(tile_order, states, width):
    return (tuple(itertools.islice(zip(tile_order, states), width * n, width * (n+1))) for n in range(width))


def check_tiles(tiles, width, tile_order, states):
    @cache
    def compare_horizontally(left, lidx, right, ridx):
        return tiles[left][lidx][3] == tiles[right][ridx][1]

    @cache
    def compare_vertically(top, top_idx, down, down_idx):
        return tiles[top][top_idx][2] == tiles[down][down_idx][0]

    for row in get_rows(tile_order, states, width):
        for left, right in zip(row, row[1:]):
            if not compare_horizontally(*left, *right):
                return False
    for row in transpose(get_rows(tile_order, states, width)):
        for top, down in zip(row, row[1:]):
            if not compare_vertically(*top, *down):
                return False
    return True


def try_combination(tiles, width, tile_order):
    for states in itertools.combinations_with_replacement(range(8), len(tile_order)):
        if check_tiles(tiles, width, tile_order, states):
            return True
    return False


def try_all_combinations(tiles):
    width = floor(sqrt(len(tiles)))
    print("Width:", width)
    for idx, position in enumerate(itertools.permutations(tiles.keys())):
        if idx % 20 == 0: print(idx)
        if try_combination(tiles, width, position):
            return position
    return None


def process(data):
    edges, tiles = rotate_tiles(data)
    r = try_all_combinations(edges)
    pprint(r)
    # part 1
    result = 0
    print("part 1:", result)
    # part 2
    result = 0
    print("part 2:", result)


def parse_tile(tile):
    header, *data = tile.split("\n")
    _, tile_id = header.split(" ")       # Tile 2729:
    tile_id = int(tile_id[:-1])
    return tile_id, data


def load_data(fileobj):
    return dict(parse_tile(t) for t in fileobj.read().split("\n\n"))


def main(file="input.txt"):
    print(file)
    with pathlib.Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    main("test.txt")
    # main()
