# https://adventofcode.com/2021/day/13
from __future__ import print_function
from pprint import pprint
from pathlib import Path
from operator import itemgetter

def render_grid(coords, dim):
    out = ""
    for line in range(dim[1] + 1):
        for col in range(dim[0] + 1):
            out += '*' if (col, line) in coords else ' '
        out += '\n'
    return out


def fold_grid(coords, dimension, axis, fold):
    def translate(val, new_high, fold):
        return new_high - abs(val - fold)
    def tuple_part(t, part, val):
        return (t[0], val) if part == 1 else (val, t[1])

    part = 0 if axis == 'x' else 1
    high = dimension[part]
    new_high = max(high - fold, fold)
    new_coords = set()
    for coord in coords:
        offset = translate(coord[part], new_high, fold)
        new_coords.add(tuple_part(coord, part, offset))
    dimension = tuple_part(dimension, part, new_high - 1)
    return new_coords, dimension


def tuple_max(iterable, part):
    return max(iterable, key=itemgetter(part))[part]


def process(data):
    coords, folds = data
    first_fold, *other_folds = folds
    dim = tuple_max(coords, 0), tuple_max(coords, 1)
    # part 1
    coords, dim = fold_grid(coords, dim, *first_fold)
    result = len(coords)
    print("part 1:", result)
    # part 2
    for f in other_folds:
        coords, dim = fold_grid(coords, dim, *f)
    print(render_grid(coords, dim))
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
    return list(map(parse_fold, section.rstrip().split('\n')))


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
