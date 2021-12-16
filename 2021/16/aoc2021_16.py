# https://adventofcode.com/2021/day/16
from __future__ import print_function
from pathlib import Path
from operator import eq, gt, lt
from itertools import islice
from math import prod


def bitstream(iterable):
    """ generates stream of bits from the list of hex characters """
    for letter in iterable:
        for bit in format(int(letter, 16), "04b"):
            yield bit


def take(iterable, length):
    """ returns a string of bits of requested count """
    return ''.join(islice(iterable, length))


def unpack(bits):
    """ converts the bits into a corresponding number """
    return int(bits, 2)


def parse_packet(stream, level=0):
    version = unpack(take(stream, 3))
    id = unpack(take(stream, 3))
    if id == 4: # literal num
        last = False
        bitnum = ""
        while not last:
            last = next(stream) == '0'
            bitnum += take(stream, 4)
        return version, id, unpack(bitnum)
    # operator
    if next(stream) == '0': # length ID - 15 bits == subpacket size in bits
        sub_len = unpack(take(stream, 15))
        substream = islice(stream, sub_len)
        packets = []
        while True:
            try:
                packets.append(parse_packet(substream, level+1))
            except ValueError:
                # unpack failed, substream is exhausted
                break
        return version, id, packets
    else: # next 11 bits == number of subpackets
        subpackets = unpack(take(stream, 11))
        packets = list(parse_packet(stream, level+1) for _ in range(subpackets))
        return version, id, packets


def sum_packet_versions(packet):
    version, _,  value = packet
    if isinstance(value, list):
        return version + sum(map(sum_packet_versions, value))
    return version


def eval_packets(packet):
    _, id, value = packet
    assert id in range(8), f"Unexpected packet id {id}"
    if id == 4: # literal
        return value
    subexpr = map(eval_packets, value)
    if id == 0: # sum
        return sum(subexpr)
    if id == 1: # product
        return prod(subexpr)
    if id == 2: # min
        return min(subexpr)
    if id == 3: # product
        return max(subexpr)
    if id == 5: # greater then
        return gt(*subexpr)
    if id == 6: # less then
        return lt(*subexpr)
    if id == 7: # equal
        return eq(*subexpr)


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
