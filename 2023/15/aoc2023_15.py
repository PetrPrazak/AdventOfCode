# https://adventofcode.com/2023/day/15
from pathlib import Path
import time


def hash(s):
    total = 0
    for c in s:
        total = (17 * (total + ord(c))) % 256
    return total


def fill_boxes(data):
    # dict() is ordered since Python 3.7
    boxes = [dict() for _ in range(256)]
    for s in data:
        if s[-1] == '-':
            label = s[:-1]
            d = boxes[hash(label)]
            if label in d:
                del d[label]
        else:
            label, val = s.split('=')
            boxes[hash(label)][label] = int(val)
    return boxes


def process(data):
    # part 1
    result = sum(hash(s) for s in data)
    print("part 1:", result)
    # part 2
    boxes = fill_boxes(data)
    result = sum(b * val * i for b, box in enumerate(boxes, 1)
                 for i, val in enumerate(box.values(), 1))
    print("part 2:", result)


def load_data(fileobj):
    return list(fileobj.read().strip().split(','))


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
