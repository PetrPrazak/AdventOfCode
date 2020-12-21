# https://adventofcode.com/2020/day/20
from __future__ import print_function
from pprint import pprint
from pathlib import Path
from collections import Counter, defaultdict
from math import floor, sqrt, prod
from copy import deepcopy
from enum import IntEnum


def transpose(matrix):
    return zip(*matrix)


def rotate_tile(tile):
    return [''.join(reversed(r)) for r in transpose(tile)]


def flip_tile(tile):
    return [''.join(reversed(l)) for l in tile]


def strmap(lmap):
    return [''.join(row) for row in lmap]


def listmap(smap):
    return [list(row) for row in smap]


def edge(row):
    return int(''.join('1' if p == '#' else '0' for p in row), 2)


class Edge(IntEnum):
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3


def edges(tile):
    top = edge(tile[0])
    down = edge(tile[-1])
    rotated = rotate_tile(tile)
    left = edge(rotated[0])
    right = edge(rotated[-1])
    return [top, right, down, left]


def remove_borders(tile):
    return [line[1:-1] for line in tile[1:-1]]


def make_all_tiles(tiles):
    all_tiles = dict()
    all_edges = dict()
    for id, tile in tiles.items():
        variants = [tile]
        for _ in range(3):
            tile = rotate_tile(tile)
            variants.append(tile)
        variants.extend([flip_tile(tile) for tile in variants])
        all_edges[id] = [edges(tile) for tile in variants]
        all_tiles[id] = [remove_borders(tile) for tile in variants]
    return all_edges, all_tiles


def find_corners(edges):
    c = Counter()
    for states in edges.values():
        for state in states:
            c.update(state)
    margin_edges = set(n for n in c if c[n] == 4)
    corner_tiles = []
    for tile, states in edges.items():
        for i, state in enumerate(states):
            if sum(bool(x in margin_edges) for x in state) == 2:
                corner_tiles.append((tile, i))
    return corner_tiles


def find_tiles(edges, exclude, value, edge):
    """ finds tiles that have a certain value on requested edge.
    returns tile id and the state index
    """
    for tile, states in edges.items():
        if tile == exclude:
            continue
        for i, state in enumerate(states):
            if state[edge] == value:
                yield tile, i


def tile_index(width, x, y):
    return y * width + x


def rec_delete(tiles_order, idx, key):
    if key in tiles_order[idx]:
        for pos, tile_variant in tiles_order[idx][key]:
            rec_delete(tiles_order, pos, tile_variant)
        del tiles_order[idx][key]


def build_candidates(edges, width, corner_tiles):
    tiles_order = [defaultdict(list) for _ in range(len(edges))]
    tiles_order[0] = {c: [] for c in corner_tiles}
    for y in range(width):
        for x in range(width):  # try to connect the first row
            idx = tile_index(width, x, y)
            del_keys = []
            for tile_variant in tiles_order[idx]:
                tile, edges_index = tile_variant
                _, right, bottom, _ = edges[tile][edges_index]
                # looking tile to match right side on the left
                if x < width - 1:
                    found = False
                    for p in find_tiles(edges, tile, right, Edge.LEFT):
                        found = True
                        # backlink
                        l = tiles_order[tile_index(width, x + 1, y)][p]
                        l.append((idx, tile_variant))
                    if not found:
                        del_keys.append(tile_variant)

                # looking tile to match bottom side on the top
                if y < width - 1:
                    found = False
                    for p in find_tiles(edges, tile, bottom, Edge.TOP):
                        found = True
                        l = tiles_order[tile_index(width, x, y + 1)][p]
                        l.append((idx, tile_variant))
                    if not found:
                        del_keys.append(tile_variant)

            for k in del_keys:
                rec_delete(tiles_order, idx, k)
    return tiles_order


def eliminate(edges, tiles_order, width):
    # eliminate from botttom up
    for tile in tiles_order[-1]:  # will be only one
        test_order = deepcopy(tiles_order)
        keys = list(test_order[-1].keys())
        keys.remove(tile)
        for k in keys:
            rec_delete(test_order, -1, k)
        return test_order


def normalize(order):
    return [list(s.keys())[0] for s in order]


def make_image(tiles, order, width):
    tile_size = 8
    rows = [[] for _ in range(width * tile_size)]
    for y in range(width):
        row = y * tile_size
        for x in range(width):
            idx = tile_index(width, x, y)
            tile, variant = order[idx]
            for r, line in enumerate(tiles[tile][variant]):
                rows[row + r].extend(line)
    return strmap(rows)


monster = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   ",
]


def make_monster_pattern():
    return [(x, y) for y, row in enumerate(monster)
            for x, c in enumerate(row) if c == '#']


def mask_pattern(smap, pattern):
    amap = listmap(smap)
    height = len(amap)
    width = len(amap[0])
    max_y = max(pattern, key=lambda t: t[1])[1]
    max_x = max(pattern)[0]
    found = False
    for y in range(height - max_y):
        for x in range(width-max_x):
            if all(amap[y+py][x + px] == '#' for px, py in pattern):
                found = True
                for px, py in pattern:
                    amap[y+py][x + px] = 'O'
    return found, amap


def find_pattern(smap, pattern):
    for _ in range(4):
        found, amap = mask_pattern(smap, pattern)
        if found:
            return strmap(amap)
        smap = flip_tile(smap)
        found, amap = mask_pattern(smap, pattern)
        if found:
            return strmap(amap)
        smap = flip_tile(smap)
        smap = rotate_tile(smap)
    return None


def process(data):
    edges, tiles = make_all_tiles(data)
    # part 1
    corner_tiles = find_corners(edges)
    result = prod(set(val for val, _ in corner_tiles))
    print("part 1:", result)

    # part 2
    width = floor(sqrt(len(edges)))
    tiles_order = build_candidates(edges, width, corner_tiles)
    correct_order = eliminate(edges, tiles_order, width)
    correct_order = normalize(correct_order)

    whole_map = make_image(tiles, correct_order, width)
    if found := find_pattern(whole_map, make_monster_pattern()):
        whole_map = found
    else:
        print("Not found")

    ctr = Counter()
    for row in whole_map:
        ctr.update(row)
    result = ctr['#']
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
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    main("test.txt")
    main()
