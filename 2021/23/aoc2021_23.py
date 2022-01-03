# https://adventofcode.com/2021/day/23
from __future__ import print_function
from pathlib import Path
from itertools import count, repeat
from heapq import heappush, heappop
from math import inf as INFINITY

EMPTY = '.'
PODS = 'ABCD'


def listit(t):
    """ converts nested tuples to nested lists """
    return list(map(listit, t)) if isinstance(t, (list, tuple)) else t


def tupleit(t):
    """ converts nested lists to nested tuples """
    return tuple(map(tupleit, t)) if isinstance(t, (list, tuple)) else t


def parse_state(data):
    """ creates the initial state of the game """
    boxes = [list() for _ in range(4)]
    for line in data[2:-1]:
        for i, idx in zip(count(0), range(3, 10, 2)):
            boxes[i].append(line[idx])
    hallway = tuple(data[1][1:12])
    return tuple(tuple(b) for b in boxes), hallway


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
    return PODS.index(pod)


def pod_steps_cost(pod, steps):
    return steps * 10 ** pod_class(pod)


def move_pod(state, burrow_idx, burrow_pos, hall_pos):
    """ swaps the content of specific burrow and a hallway """
    burrows, hallway = state
    burrow_list = listit(burrows)
    hallway_list = listit(hallway)
    h, b = hallway_list[hall_pos], burrow_list[burrow_idx][burrow_pos]
    burrow_list[burrow_idx][burrow_pos] = h
    hallway_list[hall_pos] = b
    return tupleit(burrow_list), tupleit(hallway_list)


def game_moves(state):
    burrows, hallway = state
    # check if a pod can move from the hallway to its burrow
    for h_idx, pod in enumerate(hallway):
        if pod == EMPTY:
            continue
        target_burrow = pod_class(pod)
        burrow = burrows[target_burrow]
        if any(b != EMPTY and b != pod for b in burrow):
            # can't move if not empty of other pods still there
            continue
        target_door_idx = (1 + target_burrow) * 2
        if h_idx < target_door_idx:
            # check if hallway is clear to the right
            if any(hallway[i] != EMPTY for i in range(h_idx+1, target_door_idx)):
                continue
        else:
            # check if hallway is clear to the left
            if any(hallway[i] != EMPTY for i in range(target_door_idx+1, h_idx)):
                continue
        # find the last empty burrow position
        pod_idx = 0
        while pod_idx < len(burrow) and burrow[pod_idx] == EMPTY:
            pod_idx += 1
        pod_idx -= 1
        # calculate the cost of the move
        steps = abs(h_idx - target_door_idx) + pod_idx + 1
        cost = pod_steps_cost(pod, steps)
        yield move_pod(state, target_burrow, pod_idx, h_idx), cost

    # now check if any pod can move to any hallway place
    for b_idx, burrow in enumerate(burrows):
        for pod_idx, pod in enumerate(burrow):
            if pod == EMPTY:
                continue
            target_burrow = pod_class(pod)
            if target_burrow == b_idx:
                # we are already in the right burrow
                if all(b == EMPTY or b == pod for b in burrow):
                    continue
            if any(burrow[i] != EMPTY for i in range(pod_idx-1, -1, -1)):
                # can't get out from burrow
                continue
            for h_idx, h_place in enumerate(hallway):
                if h_idx in range(2, 10, 2):
                    # can't stand in any door
                    continue
                if h_place != EMPTY:
                    # hallway not empty
                    continue
                h_door_idx = (1 + b_idx) * 2
                if h_idx < h_door_idx:
                    # check if hallway is clear to the left
                    if any(hallway[i] != EMPTY for i in range(h_idx, h_door_idx)):
                        continue
                else:
                    # check if hallway is clear to the right
                    if any(hallway[i] != EMPTY for i in range(h_door_idx+1, h_idx)):
                        continue
                # calculate the cost of the move
                steps = pod_idx + abs(h_idx - h_door_idx) + 1
                cost = pod_steps_cost(pod, steps)
                yield move_pod(state, b_idx, pod_idx, h_idx), cost


def play(data):
    start_state = parse_state(data)
    burrow_len = len(start_state[0][0])
    end_burrows = tuple(tuple(repeat(pod, burrow_len)) for pod in PODS)
    end_state = end_burrows, start_state[1]
    return dijkstra(start_state, end_state, game_moves)


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
