# https://adventofcode.com/2024/day/5
from pathlib import Path
from collections import defaultdict
import time


def process(data):
    # part 1
    rules, pages = data
    ordering = defaultdict(set)
    for before, page in rules:
        ordering[page].add(before)
    total = 0
    wrong_pages = []
    for page in pages:
        to_print = set(page)
        for p in page:
            if ordering[p].intersection(to_print):
                wrong_pages.append(page)
                break
            to_print.remove(p)
        else:
            total += page[len(page)//2]

    print("part 1:", total)
    # part 2
    total = 0
    for page in wrong_pages:
        ok = False
        while not ok:
            for idx, (p1, p2) in enumerate(zip(page, page[1:])):
                if p2 in ordering[p1]:
                    # swap and try again
                    page[idx:idx+2] = [p2, p1]
                    break
            else:
                ok = True
        total += page[len(page)//2]

    print("part 2:", total)


def load_data(fileobj):
    rules, pages = fileobj.read().split("\n\n")
    rules = [[int(n) for n in row.split('|')] for row in rules.split('\n')]
    pages = [[int(n) for n in row.split(',')] for row in pages.split('\n')]
    return rules, pages


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
