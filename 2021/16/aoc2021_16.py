# https://adventofcode.com/2021/day/16
from __future__ import print_function
from pprint import pprint
from pathlib import Path
from operator import eq, gt, lt
from itertools import islice
from string import digits
from math import prod


def bitstream(iterable):
    for letter in iterable:
        if letter in digits:
            num = ord(letter) - ord('0')
        else:
            num = ord(letter) - ord('A') + 10
        bits = bin(num)[2:]
        for _ in range(4 - len(bits)):
            yield "0"
        for bit in bits:
            yield bit


def take(iterable, length):
    """ returns bits of requested count """
    return ''.join(islice(iterable, length))


def pack(iterable):
    """ converts the bits into a corresponding number """
    s = ''.join(iterable)
    if not s: raise StopIteration
    return int(s, 2)


def parse_packet(stream, level=0):
    version = pack(take(stream, 3))
    id = pack(take(stream, 3))
    if id == 4: # literal num
        last = False
        bitnum = []
        while not last:
            last = next(stream) == '0'
            bitnum.append(take(stream, 4))
        return version, id, pack(bitnum)
    else: # operator
        if next(stream) == '0': # length ID - 15 bits == subpacket size in bits
            sub_len = pack(take(stream, 15))
            substream = iter(take(stream, sub_len))
            packets = []
            while True:
                try:
                    packets.append(parse_packet(substream, level+1))
                except StopIteration:
                    break
            return version, id, packets
        else: # next 11 bits == number of subpackets
            packets = pack(take(stream, 11))
            return version, id, list(parse_packet(stream, level+1) for _ in range(packets))


def sum_packet_versions(packet):
    version, _,  value = packet
    if isinstance(value, list):
        return version + sum(map(sum_packet_versions, value))
    else:
        return version


def eval_packets(packet):
    _, id, value = packet
    if isinstance(value, list):
        if id == 0: # sum
            return sum(map(eval_packets, value))
        elif id == 1: # product
            return prod(map(eval_packets, value))
        elif id == 2: # min
            return min(map(eval_packets, value))
        elif id == 3: # product
            return max(map(eval_packets, value))
        elif id == 5: # greater then
            assert(len(value) == 2)
            return gt(*map(eval_packets, value))
        elif id == 6: # less then
            assert(len(value) == 2)
            return lt(*map(eval_packets, value))
        elif id == 7: # equal
            assert(len(value) == 2)
            return eq(*map(eval_packets, value))
        else:
            assert 0, f"unknown id {id}"
    else:
        return value


def test():
    assert sum_packet_versions(parse_packet(bitstream("C0015000016115A2E0802F182340"))) == 23
    assert sum_packet_versions(parse_packet(bitstream("A0016C880162017C3686B18A3D4780"))) == 31
    assert eval_packets(parse_packet(bitstream("9C0141080250320F1802104A08"))) == 1
    assert eval_packets(parse_packet(bitstream("CE00C43D881120"))) == 9


def process(data):
    # part 1
    packet = parse_packet(bitstream(data))
    print("part 1:", sum_packet_versions(packet))
    # part 2
    print("part 2:", eval_packets(packet))


def load_data(fileobj):
    return fileobj.readline().strip()


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # test()
    main()
