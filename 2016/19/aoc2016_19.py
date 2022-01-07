# https://adventofcode.com/2016/day/19
from __future__ import print_function
from pathlib import Path
from collections import deque


def part1(num):
    players = deque(range(1, num+1))
    while len(players) > 1:
        players.rotate(-1)
        players.popleft()
    return players[0]


def part2slow(num):
    """ way too slow :(
    deque.rotate(k) is actually O(k) !!! """
    players = deque(range(1, num+1))
    while len(players) > 1:
        across = len(players)//2
        players.rotate(-across)
        removed = players.popleft()
        players.rotate(across - 1)
    return players[0]


class ElfTable:
    class Node:
        def __init__(self, value) -> None:
            self.value = value
            self.prev = None
            self.next = None

    def __init__(self, iter=None) -> None:
        self.start = None
        self.mid = None
        self.length = 0
        if iter:
            for val in iter:
                self.append(val)

    def append(self, value) -> None:
        node = ElfTable.Node(value)
        if not self.start:
            node.next = node
            node.prev = node
            self.start = self.mid = node
        else:
            self.start.prev.next = node
            node.prev = self.start.prev
            node.next = self.start
            self.start.prev = node
            self.length += 1
            if self.length % 2 == 0:
                self.mid = self.mid.next

    def remove_mid(self):
        val = self.mid.value
        self.mid.next.prev = self.mid.prev
        self.mid.prev.next = self.mid.next
        self.length -= 1
        if self.length % 2 == 0:
            self.mid = self.mid.prev
        else:
            self.mid = self.mid.next
        return val

    def rotate(self):
        self.start = self.start.next
        self.mid = self.mid.next

    def play(self):
        while self.length > 1:
            self.remove_mid()
            self.rotate()
        return self.start.value


def part2(num):
    table = ElfTable(range(1, num+1))
    return table.play()


def process(data):
    # part 1
    result = part1(data)
    print("part 1:", result)
    # part 2
    result = part2(data)
    print("part 2:", result)


def load_data(fileobj):
    return int(fileobj.read())


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
