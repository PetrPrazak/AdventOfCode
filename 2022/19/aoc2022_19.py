# https://adventofcode.com/2022/day/19
from pathlib import Path
from collections import deque
from math import prod
import time
import re


def best_case_scenario(initial_amount, robots, t):
    return initial_amount + robots * (t + 1) + t * (t + 1) // 2


def mine_geodes(blueprint, time=24):
    (
        r_ore_ore,
        r_clay_ore,
        r_obs_ore,
        r_obs_clay,
        r_geode_ore,
        r_geode_obs,
    ) = blueprint

    max_geodes = 0
    max_ore_needed = max(r_ore_ore, r_clay_ore, r_obs_ore, r_geode_ore)
    max_clay_needed = r_obs_clay
    max_obs_needed = r_geode_obs

    visited = set()
    q = deque([(time, 0, 0, 0, 0, 1, 0, 0, 0)])

    while q:
        time, ore, clay, obs, geode, r_ore, r_clay, r_obs, r_geode = state = q.pop()
        if state in visited:
            continue
        visited.add(state)

        newore = ore + r_ore
        newclay = clay + r_clay
        newobs = obs + r_obs
        newgeode = geode + r_geode
        time -= 1

        if time == 0:
            max_geodes = max(max_geodes, newgeode)
            continue

        # If we can't mine more geodes in the best-case scenario, bail out.
        if best_case_scenario(newgeode, r_geode, time) < max_geodes:
            continue

        # If we can't mine enough obsidian to build new geode robots even in the
        # best-case scenario, we already know how many geodes we'll be able to get.
        if (
            best_case_scenario(newobs, r_obs, time) < r_geode_obs
            or best_case_scenario(newore, r_ore, time) < r_geode_ore
        ):
            max_geodes = max(max_geodes, newgeode + r_geode * time)
            continue

        # if (
        #     (r_obs and obs < max_obs_needed)
        #     or (r_clay and clay < max_clay_needed)
        #     or ore < max_ore_needed
        # ):
        # mining, no new robots
        q.append(
            (time, newore, newclay, newobs, newgeode, r_ore, r_clay, r_obs, r_geode)
        )

        # can build geode robot?
        if obs >= r_geode_obs and ore >= r_geode_ore:
            q.append(
                (
                    time,
                    newore - r_geode_ore,
                    newclay,
                    newobs - r_geode_obs,
                    newgeode,
                    r_ore,
                    r_clay,
                    r_obs,
                    r_geode + 1,
                )
            )
        # can build obsidian robot?
        if clay >= r_obs_clay and ore >= r_obs_ore:  # and obs < max_obs_needed:
            q.append(
                (
                    time,
                    newore - r_obs_ore,
                    newclay - r_obs_clay,
                    newobs,
                    newgeode,
                    r_ore,
                    r_clay,
                    r_obs + 1,
                    r_geode,
                )
            )
        # can build clay robot?
        if ore >= r_clay_ore:  # and clay < max_clay_needed:
            q.append(
                (
                    time,
                    newore - r_clay_ore,
                    newclay,
                    newobs,
                    newgeode,
                    r_ore,
                    r_clay + 1,
                    r_obs,
                    r_geode,
                )
            )
        # can build ore robot?
        if ore >= r_ore_ore:  # and ore < max_ore_needed:
            q.append(
                (
                    time,
                    newore - r_ore_ore,
                    newclay,
                    newobs,
                    newgeode,
                    r_ore + 1,
                    r_clay,
                    r_obs,
                    r_geode,
                )
            )
    print(max_geodes)
    return max_geodes


ORE, CLAY, OBS, GEO = range(4)


def search(blueprint, time=24):
    (
        rore_cost,
        rclay_cost,
        robs_cost_ore,
        robs_cost_clay,
        rgeo_cost_ore,
        rgeo_cost_obs,
    ) = blueprint
    max_ore_needed = max(rore_cost, rclay_cost, robs_cost_ore, rgeo_cost_ore)
    max_clay_needed = robs_cost_clay
    max_obs_needed = rgeo_cost_obs

    best = 0
    visited = set()
    q = deque([(time, 0, 0, 0, 0, 1, 0, 0, 0, ())])

    while q:
        tmp = q.pop()

        state = tmp[:-1]
        if state in visited:
            continue

        visited.add(state)

        time, ore, clay, obs, geo, rore, rclay, robs, rgeo, did_not_build = tmp
        newore = ore + rore
        newclay = clay + rclay
        newobs = obs + robs
        newgeo = geo + rgeo
        time -= 1

        if time == 0:
            best = max(best, newgeo)
            continue

        if best_case_scenario(newgeo, rgeo, time) < best:
            continue

        if (
            best_case_scenario(newobs, robs, time) < rgeo_cost_obs
            or best_case_scenario(newore, rore, time) < rgeo_cost_ore
        ):
            best = max(best, newgeo + rgeo * time)
            continue

        can_build = []

        if obs >= rgeo_cost_obs and ore >= rgeo_cost_ore and GEO not in did_not_build:
            can_build.append(GEO)
            q.append(
                (
                    time,
                    newore - rgeo_cost_ore,
                    newclay,
                    newobs - rgeo_cost_obs,
                    newgeo,
                    rore,
                    rclay,
                    robs,
                    rgeo + 1,
                    (),
                )
            )

        if (
            robs < max_obs_needed
            and clay >= robs_cost_clay
            and ore >= robs_cost_ore
            and OBS not in did_not_build
        ):
            can_build.append(OBS)
            q.append(
                (
                    time,
                    newore - robs_cost_ore,
                    newclay - robs_cost_clay,
                    newobs,
                    newgeo,
                    rore,
                    rclay,
                    robs + 1,
                    rgeo,
                    (),
                )
            )

        if rclay < max_clay_needed and ore >= rclay_cost and CLAY not in did_not_build:
            can_build.append(CLAY)
            q.append(
                (
                    time,
                    newore - rclay_cost,
                    newclay,
                    newobs,
                    newgeo,
                    rore,
                    rclay + 1,
                    robs,
                    rgeo,
                    (),
                )
            )

        if rore < max_ore_needed and ore >= rore_cost and ORE not in did_not_build:
            can_build.append(ORE)
            q.append(
                (
                    time,
                    newore - rore_cost,
                    newclay,
                    newobs,
                    newgeo,
                    rore + 1,
                    rclay,
                    robs,
                    rgeo,
                    (),
                )
            )

        if (
            (robs and obs < max_obs_needed)
            or (rclay and clay < max_clay_needed)
            or ore < max_ore_needed
        ):
            q.append(
                (
                    time,
                    newore,
                    newclay,
                    newobs,
                    newgeo,
                    rore,
                    rclay,
                    robs,
                    rgeo,
                    can_build,
                )
            )
    print(best)
    return best


def process(data):
    # part 1
    result = sum(bid * search(bp) for bid, *bp in data)
    print("part 1:", result)
    # part 2
    result = prod(search(bp, time=32) for _, *bp in data[:3])
    print("part 2:", result)


def parse_line(line):
    return tuple(map(int, re.findall("\d+", line)))


def load_data(fileobj):
    return [parse_line(line.rstrip()) for line in fileobj.readlines()]


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
