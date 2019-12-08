# https://adventofcode.com/2019/day/08

from __future__ import print_function
from collections import Counter

INPUT = "aoc2019_08_input.txt"

cat = ''.join


def get_layer(data, pos, width, height):
    return data[pos: pos + width * height]


def print_image(image, width, height):
    output = ['#' if p is 1 else ' ' for p in image]
    for h in range(height):
        print(cat(output[h * width: (h + 1) * width]))


def process(data, size):
    data = [int(d) for d in data]

    width, height = size
    area = width * height

    min0 = area
    min0digits = None
    layers_count = len(data) // area
    image = [2] * area

    for i in range(layers_count):
        layer = get_layer(data, i * area, width, height)
        d = Counter(layer)
        if d[0] < min0:
            min0 = d[0]
            min0digits = d
        # part 2
        for (pos, bit) in enumerate(layer):
            if image[pos] == 2:
                image[pos] = bit

    # part 1
    print(min0digits[1] * min0digits[2])
    # part 2
    print_image(image, width, height)


def test():
    process("123456789012", (3, 2))
    process("0222112222120000", (2, 2))


def main():
    with open(INPUT) as f:
        data = f.readline().rstrip()
        process(data, (25, 6))


if __name__ == "__main__":
    # test()
    main()
