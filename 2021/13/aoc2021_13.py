# https://adventofcode.com/2021/day/13
from __future__ import print_function
from pprint import pprint
from pathlib import Path
from functools import reduce

def minmax_tuples(tuple_list, element=0):
    res = sorted(tuple_list, key=lambda k: k[element])
    return res[0][element], res[-1][element]


def render_grid(coords, on='*', off=' '):
    min_x, max_x = minmax_tuples(coords, 0)
    min_y, max_y = minmax_tuples(coords, 1)
    out = ""
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            out += on if (x, y) in coords else off
        out += '\n'
    return out


def tuple_part(t, part, val):
    """ returns the original tuple with specific part replaced """
    tuple_list = list(t)
    tuple_list[part] = val
    return tuple(tuple_list)


def fold_grid(coords, fold_instr):
    part, fold = fold_instr[0] == 'y', fold_instr[1]
    return {tuple_part(coord, part, fold - abs(coord[part] - fold)) for coord in coords}


def process(data):
    coords, folds = data
    first_fold, *other_folds = folds
    # part 1
    coords = fold_grid(coords, first_fold)
    result = len(coords)
    print("part 1:", result)
    # part 2
    coords = reduce(fold_grid, other_folds, coords)
    print(render_grid(coords))
    result = "just read the output :)"  # here comes OCR :D
    print("part 2:", result)


def parse_coords(section):
    def parse_coord(line):
        return tuple(map(int, line.split(',')))
    return list(map(parse_coord, section.split('\n')))


def parse_folds(section):
    def parse_fold(line):
        instr, val = line.split('=')
        return instr[-1], int(val)
    return list(map(parse_fold, section.strip().split('\n')))


def load_data(fileobj):
    coords, folds = fileobj.read().split("\n\n")
    return parse_coords(coords), parse_folds(folds)


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
