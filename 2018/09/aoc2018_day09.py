# https://adventofcode.com/2018/day/9

from __future__ import print_function
from collections import defaultdict
from time import  time

INPUT = "aoc2018_day09.txt"


def play(players, last_marble):
    print(players, last_marble)
    current = 0
    desk = list()
    desk.append(0)
    cur_len = 1
    player = 0
    score = defaultdict(list)
    last_time = time()
    for marble in range(1, last_marble+1):
        # cur_len = len(desk)
        if marble % 100000 == 0:
            next_time = time()
            print(next_time - last_time, marble)
            last_time = next_time

        if not marble % 23:
            score[player].append(marble)
            keep = (current + cur_len - 6) % cur_len
            score[player].append(desk[keep])
            del desk[keep]
            current = keep - 1
            cur_len -= 1
        else:
            current = (current + 2) % cur_len
            desk.insert(current+1, marble)
            cur_len += 1

        player = (player + 1) % players

    score_count = [(sum(score[p]), p) for p in score]
    # print(score_count)
    return max(score_count)

# test data
# 0 players; last marble is worth 1618 points: high score is 8317
# 13 players; last marble is worth 7999 points: high score is 146373
# 17 players; last marble is worth 1104 points: high score is 2764
# 21 players; last marble is worth 6111 points: high score is 54718
# 30 players; last marble is worth 5807 points: high score is 37305

with open(INPUT) as f:
    data = f.readline().rstrip().split()
    # print(play(9, 25))
    # print(play(10, 1618))
    # print(play(13,7999))
    # print(play(30,5807))
    print(play(int(data[0]), int(data[6])))
    print(play(int(data[0]), int(data[6]) * 100))
