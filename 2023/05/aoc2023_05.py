# https://adventofcode.com/2023/day/5
from pprint import pprint
from pathlib import Path
from collections import deque
import time


def map_range(src, dst_start, src_start, len):
    if src >= src_start and src < src_start + len:
        return dst_start + src - src_start
    return None


def convert(mappings, num):
    for mapping in mappings:
        for rmap in mapping:
            if c := map_range(num, *rmap):
                num = c
                break
    return num


def part1(seeds, mappings):
    min_loc = float('inf')
    for num in seeds:
        num = convert(mappings, num)
        min_loc = min(num, min_loc)
    return min_loc


def part2(seeds, mappings):
    segments = deque((v, v + n) for v, n in zip(seeds[::2], seeds[1::2]))
    for mapping in mappings:
        processed = deque()
        while segments:
            a, b = segments.popleft()
            for dst, src, length in mapping:
                c, d = src, src + length
                delta = dst - src
                partial_left = c <= a < d
                partial_right = c < b <= d

                if partial_left and partial_right:
                    # Complete overlap:
                    #     a---b
                    # c-----------d
                    # Entire [a, b) segment is converted
                    processed.append((a + delta, b + delta))
                    break
                if partial_left:
                    # Partial left overlap:
                    #     a------b
                    # c------d
                    # [a, d) is converted
                    processed.append((a + delta, d + delta))
                    segments.append((d, b))
                    break
                if partial_right:
                    # Partial right overlap:
                    # a------b
                    #     c------d
                    # [c, b) is converted
                    processed.append((c + delta, b + delta))
                    segments.append((a, c))
                    break
                if a < c and b > d:
                    # Partial inner overlap:
                    # a-----------b
                    #     c---d
                    # [c, d) is converted
                    processed.append((c + delta, d + delta))
                    segments.append((a, c))
                    segments.append((d, b))
                    break
            else:
                # no overlap, keep as is
                processed.append((a, b))
        segments = processed
    return min(s[0] for s in segments)


def process(data):
    # part 1
    seeds, *mappings = data
    seeds = seeds[0]
    result = part1(seeds, mappings)
    print("part 1:", result)

    # part 2
    result = part2(seeds, mappings)
    print("part 2:", result)


def numlist(s):
    return list(map(int, s.split()))


def parse_section(section):
    header, section = section.split(':')
    return list(map(numlist, section.strip().split('\n')))


def load_data(fileobj):
    return [parse_section(part) for part in fileobj.read().split("\n\n")]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        t1 = time.perf_counter()
        process(load_data(f))
        t2 = time.perf_counter()
        print(f"Finished in {t2 - t1:.3f} s")


if __name__ == "__main__":
    main("test.txt")
    main()
