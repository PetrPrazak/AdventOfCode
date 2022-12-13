# https://adventofcode.com/2022/day/13
from pprint import pprint
from pathlib import Path
import logging
from functools import cmp_to_key
from math import prod


def compare_lists(l1, l2, indent=''):
    logging.info(f"{indent}- Compare {l1} vs {l2}")
    for idx in range(max(len(l1), len(l2))):
        if idx == len(l1):
            logging.info(
                f"  {indent}- Left side ran out of items, so inputs are in the right order")
            return True
        if idx == len(l2):
            logging.info(
                f"  {indent}- Right side ran out of items, so inputs are not in the right order")
            return False  # not right order
        item1, item2 = l1[idx], l2[idx]
        if type(item1) is int and type(item2) is int:
            logging.info(f"  {indent}- Compare {item1} vs {item2}")
            if item1 != item2:
                if item1 < item2:
                    logging.info(
                        f"  {indent}- Left side is smaller, so inputs are in the right order")
                    return True
                else:
                    logging.info(
                        f"  {indent}- Right side is smaller, so inputs are not in the right order")
                    return False
            continue
        if type(item1) is not list:
            item1 = [item1]
        if type(item2) is not list:
            item2 = [item2]
        list_compare = compare_lists(item1, item2, indent+'  ')
        if list_compare is None:
            continue
        return list_compare
    return None


def packets_cmp(l1, l2):
    if compare_lists(l1, l2):
        return -1
    if compare_lists(l2, l1):
        return 1
    return 0


def process(data):
    # part 1
    result = sum(idx for idx, val in
                 enumerate((compare_lists(l1, l2) for l1, l2 in data), start=1)
                 if val)
    print("part 1:", result)
    # part 2
    packets = [packet for pair in data for packet in pair]
    div_packets = [[[2]], [[6]]]
    packets += div_packets
    packets.sort(key=cmp_to_key(packets_cmp))
    div_indices = [idx for idx, packet in enumerate(packets, start=1)
                   if packet in div_packets]
    print("part 2:", prod(div_indices))


#
#   <line> -> list
#   <list> -> '[' items ']'
#   <items> -> e | <item> | <item> ',' <item>
#   <item> -> list | number
#   <number> -> '[0-9]' | '[0-9]' <number>
#


def parse_num(line, pos):
    ret = 0
    while (c := line[pos]).isdigit():
        ret *= 10
        ret += int(c)
        pos += 1
    return ret, pos


def parse_items(line, pos):
    if pos >= len(line):
        return None, pos
    if line[pos] == '[':
        l, pos = parse_list(line, pos)
        assert line[pos] == ']'
        return l, pos+1
    if line[pos].isdigit():
        return parse_num(line, pos)
    if line[pos] == ']':
        return None, pos


def parse_list(line, pos=0):
    assert line[pos] == '['
    ret = list()
    pos += 1
    while True:
        item, pos = parse_items(line, pos)
        if item is None:
            break
        ret.append(item)
        if line[pos] != ',':
            break
        pos += 1
    return ret, pos


def parse_line(line):
    l, _ = parse_list(line)
    line = line.replace(",", ", ")
    assert line == str(l)
    return l


def parse_section(section):
    return tuple(map(parse_line, section.split('\n')))


def load_data(fileobj):
    return [parse_section(section) for section in fileobj.read().split("\n\n")]


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    main("test.txt")
    main()
