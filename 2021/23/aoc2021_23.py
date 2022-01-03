# https://adventofcode.com/2021/day/23
from __future__ import print_function
from pathlib import Path
from itertools import count, repeat, chain
from heapq import heappush, heappop
from math import inf as INFINITY
from functools import partial

EMPTY = 0
PODS = 'ABCD'


def parse_state(data):
    """ creates the initial state of the game """
    burrow_lines = data[2:-1]
    burrow_size = len(burrow_lines)
    boxes = [0] * (burrow_size * 4)
    for i, idx in zip(count(0), range(3, 10, 2)):
        for l, line in enumerate(burrow_lines):
            boxes[burrow_size * i + l] = PODS.index(line[idx]) + 1
    hallway = tuple([0] * 11)
    return tuple(boxes), hallway


def dijkstra(start, target, moves_f):
    path_cost = {start: 0}  # The cost of the best path to a state.
    pq = [(0, start)]
    while pq:
        total, current = heappop(pq)
        if current == target:
            return total
        for neighbor, value in moves_f(current):
            new_cost = path_cost[current] + value
            if new_cost < path_cost.get(neighbor, INFINITY):
                heappush(pq, (new_cost, neighbor))
                path_cost[neighbor] = new_cost
    return INFINITY


def pod_class(pod):
    return pod - 1


COST = list(10 ** c for c in range(4))


def pod_steps_cost(pod, steps):
    return steps * COST[pod_class(pod)]


def move_pod(state, burrow_idx, burrow_pos, hall_pos):
    """ swaps the content of specific burrow and a hallway """
    burrows, hallway = state
    blen = len(burrows) // 4
    b_pos = burrow_idx * blen + burrow_pos
    h, b = hallway[hall_pos], burrows[b_pos]
    burrow_list = list(burrows)
    burrow_list[b_pos] = h
    hallway_list = list(hallway)
    hallway_list[hall_pos] = b
    return tuple(burrow_list), tuple(hallway_list)


def move_pod_directly(state, burrow_idx, burrow_pos, target_burrow_idx, target_burrow_pos):
    """ swaps the content of specific burrows """
    burrows, hallway = state
    blen = len(burrows) // 4
    target_pos = target_burrow_idx * blen + target_burrow_pos
    source_pos = burrow_idx * blen + burrow_pos
    b1, b2 = burrows[target_pos], burrows[source_pos]
    burrow_list = list(burrows)
    burrow_list[source_pos] = b1
    burrow_list[target_pos] = b2
    return tuple(burrow_list), hallway


def game_moves(burrow_len, state):
    burrows, hallway = state

    def is_hallway_clear(start, end):
        if start > end:
            start, end = end, start
        return sum(hallway[start+1: end]) == 0

    def last_empty_cell(burrow):
        idx = 0
        while idx < len(burrow) and burrow[idx] == EMPTY:
            idx += 1
        return idx - 1

    def can_move_home(burrow, pod):
        return all(b == EMPTY or b == pod for b in burrow)

    def door_idx(burrow_idx):
        """ mapping from burrow index to its hallway door index """
        return (1 + burrow_idx) * 2

    def get_burrow(burrow_idx):
        return burrows[burrow_idx * burrow_len: (burrow_idx + 1) * burrow_len]

    # check if a pod can move from the hallway to its burrow
    for h_idx, pod in enumerate(hallway):
        if pod == EMPTY:
            continue
        target_burrow_idx = pod_class(pod)
        burrow = get_burrow(target_burrow_idx)
        target_door_idx = door_idx(target_burrow_idx)
        if not (can_move_home(burrow, pod) and is_hallway_clear(h_idx, target_door_idx)):
            continue
        pod_idx = last_empty_cell(burrow)
        steps = abs(h_idx - target_door_idx) + pod_idx + 1
        cost = pod_steps_cost(pod, steps)
        yield move_pod(state, target_burrow_idx, pod_idx, h_idx), cost

    # now check if any pod can move to any hallway place
    for b_idx, pod in enumerate(burrows):
        if pod == EMPTY:
            continue
        b_idx, pod_idx = divmod(b_idx, burrow_len)
        burrow = get_burrow(b_idx)
        target_burrow_idx = pod_class(pod)
        if target_burrow_idx == b_idx:
            # we are already in the right burrow
            if can_move_home(burrow, pod):
                continue
        if pod_idx > 0 and any(burrow[i] != EMPTY for i in range(pod_idx-1, -1, -1)):
            # can't get out from burrow
            continue
        h_door_idx = door_idx(b_idx)
        # check if we can go directly to target burrow
        target_door_idx = door_idx(target_burrow_idx)
        target_burrow = get_burrow(target_burrow_idx)
        if can_move_home(target_burrow, pod) and is_hallway_clear(h_door_idx, target_door_idx):
            target_pos = last_empty_cell(target_burrow)
            steps = abs(h_door_idx - target_door_idx) + \
                pod_idx + target_pos + 2
            cost = pod_steps_cost(pod, steps)
            yield move_pod_directly(state, b_idx, pod_idx, target_burrow_idx, target_pos), cost
            continue

        for h_idx, h_place in enumerate(hallway):
            if h_idx in range(2, 10, 2) or h_place != EMPTY:
                # can't move to a door or an occupied place
                continue
            if not is_hallway_clear(h_idx, h_door_idx):
                # path is blocked
                continue
            steps = pod_idx + abs(h_idx - h_door_idx) + 1
            cost = pod_steps_cost(pod, steps)
            yield move_pod(state, b_idx, pod_idx, h_idx), cost


def play(data):
    start_state = parse_state(data)
    burrow_len = len(start_state[0]) // 4
    end_burrows = tuple(p for pod in range(1, 5)
                        for p in repeat(pod, burrow_len))
    end_state = end_burrows, start_state[1]
    moves = partial(game_moves, burrow_len)
    return dijkstra(start_state, end_state, moves)


def process(data):
    # part 1
    result = play(data)
    print("part 1:", result)
    # part 2
    data[3:3] = ["  #D#C#B#A#", "  #D#B#A#C#"]
    result = play(data)
    print("part 2:", result)


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(f.readlines())


if __name__ == "__main__":
    # main("test.txt")
    main()
