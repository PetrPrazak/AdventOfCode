# https://adventofcode.com/2018/day/9

from __future__ import print_function
from collections import defaultdict, deque
from time import time

INPUT = "aoc2018_day09.txt"


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class Game:
    def __init__(self):
        node = Node(0)
        node.next = node
        node.prev = node
        self.cur_node = node

    def add_marble(self, marble):
        new_node = Node(marble)
        after = self.cur_node.next
        new_node.next = after.next
        new_node.prev = after
        after.next.prev = new_node
        after.next = new_node
        self.cur_node = new_node

    def remove_marble(self):
        removed = self.cur_node
        for _ in range(7):
            removed = removed.prev
        removed.prev.next = removed.next
        removed.next.prev = removed.prev
        self.cur_node = removed.next
        return removed.data

    def print_list(self):
        next_node = self.cur_node.next
        print("[", self.cur_node.data, end="")
        while next_node != self.cur_node:
            print(",", next_node.data, end="")
            next_node = next_node.next
        print(" ]")


def play2(players, last_marble):
    print(players, last_marble)
    desk = Game()
    player = 0
    score = defaultdict(int)
    for marble in range(1, last_marble+1):
        if not marble % 23:
            removed_marble = desk.remove_marble()
            score[player] += marble + removed_marble
        else:
            desk.add_marble(marble)
        player = (player + 1) % players

    return max(score.values())


def play3(players, last_marble):
    print(players, last_marble)
    desk = deque([0])
    score = defaultdict(int)
    for marble in range(1, last_marble+1):
        if not marble % 23:
            desk.rotate(7)
            score[marble % players] += marble + desk.pop()
            desk.rotate(-1)
        else:
            desk.rotate(-1)
            desk.append(marble)

    return max(score.values())

# test data
# 10 players; last marble is worth 1618 points: high score is 8317
# 13 players; last marble is worth 7999 points: high score is 146373
# 17 players; last marble is worth 1104 points: high score is 2764
# 21 players; last marble is worth 6111 points: high score is 54718
# 30 players; last marble is worth 5807 points: high score is 37305


with open(INPUT) as f:
    data = f.readline().rstrip().split()
    # print(play2(9, 25))
    assert(play2(10, 1618) == 8317)
    assert(play2(13,7999) == 146373)
    assert(play2(30,5807) == 37305)
    print(play2(int(data[0]), int(data[6])))
    start = time()
    print(play2(int(data[0]), int(data[6]) * 100))
    end = time()
    print("my version", end - start)
    start = time()
    print(play3(int(data[0]), int(data[6]) * 100))
    end = time()
    print("deque", end - start)
