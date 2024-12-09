# https://adventofcode.com/2024/day/9
from pathlib import Path
from copy import copy
import time

EMPTY = -1


def make_blocks(data):
    fileId = 0
    blocks = []
    isEmpty = False
    for c in data:
        for _ in range(int(c)):
            blocks.append(EMPTY if isEmpty else fileId)
        if not isEmpty:
            fileId += 1
        isEmpty = not isEmpty
    return blocks


def part1(blocks):
    blocks = copy(blocks)
    first, last = 0, len(blocks) - 1
    while True:
        while first < len(blocks) and blocks[first] != EMPTY:
            first += 1
        while last > 0 and blocks[last] == EMPTY:
            last -= 1
        if first >= last:
            break
        blocks[first] = blocks[last]
        blocks[last] = EMPTY
    return blocks


def make_files(blocks):
    files = []
    s, b = 0, blocks[0]
    for pos, f in enumerate(blocks):
        if f != b:
            files.append((b, pos - s))
            s, b = pos, f
    files.append((b, pos - s + 1))
    return files


def part2(files):
    # for all files backwards
    last_file_pos = len(files) - 1
    while last_file_pos > 0:
        file, file_len = files[last_file_pos]
        if file == EMPTY:
            last_file_pos -= 1
            continue
        # search for a free, large enough block
        free_pos = 0
        while free_pos < last_file_pos:
            free_type, free_len = files[free_pos]
            if free_type == EMPTY and free_len >= file_len:
                break
            free_pos += 1
        else:
            # no block found
            last_file_pos -= 1
            continue

        # move a file to the free block
        files[free_pos] = file, file_len
        files[last_file_pos] = EMPTY, file_len

        if free_len > file_len:
            #if a free space left, merge it or add a new one
            empty_len = free_len - file_len
            free_pos += 1
            t, l = files[free_pos]
            if t == EMPTY:
                files[free_pos] = EMPTY, l + empty_len
            else:
                files.insert(free_pos, (EMPTY, empty_len))
                last_file_pos += 1

        last_file_pos -= 1


def checksum(blocks):
    return sum(i * f for i, f in enumerate(blocks) if f != EMPTY)


def checksum_files(files):
    total = 0
    pos = 0
    for f, l in files:
        if f != EMPTY:
            for i in range(pos, pos + l):
                total += f * i
        pos += l
    return total


def process(data):
    blocks = make_blocks(data)
    # part 1
    result = checksum(part1(blocks))
    print("part 1:", result)
    # part 2
    files = make_files(blocks)
    part2(files)
    # print(files)
    print("part 2:", checksum_files(files))
    print(f"{inserts=}")

def load_data(fileobj):
    return fileobj.read()


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
