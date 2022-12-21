# https://adventofcode.com/2022/day/20
from pathlib import Path
import time


class Number:
    __slots__ = 'value'

    def __init__(self, value):
        self.value = int(value)


def mix(order, times=1):
    numbers, size = list(order), len(order)

    for _ in range(times):
        for num in order:
            if num.value == 0: continue
            i = numbers.index(num)
            numbers.pop(i)
            numbers.insert((i + num.value) % (size - 1), num)

    for i, num in enumerate(numbers):
        if num.value == 0:
            break

    return sum(numbers[(i + off) % size].value for off in (1000, 2000, 3000))


def process(data):
    # part 1
    result = mix(data)
    print("part 1:", result)
    # part 2
    for num in data:
        num.value *= 811589153
    result = mix(data, 10)
    print("part 2:", result)


def load_data(fileobj):
    return tuple(Number(line.rstrip()) for line in fileobj.readlines())


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        t1 = time.perf_counter()
        process(load_data(f))
        t2 = time.perf_counter()
        print(f"Finished in {t2 - t1:.3} s")


if __name__ == "__main__":
    # main("test.txt")
    main()
