# https://adventofcode.com/2018/day/7

from __future__ import print_function
from collections import defaultdict
import re


INPUT = "aoc2018_day07.txt"
workers = 5
delay = 60
# INPUT = "test.txt"
# workers = 2
# delay = 0


def is_all_done(already_done, todo):
    for req in todo:
        if not (req in already_done):
            return False
    return True


class Factory:
    def __init__(self, workers, delay, prereq):

        self.workers = workers
        self.queue = list()
        self.delay = delay
        self.timer = 0
        self.done = set()
        self.wait_list = list()
        self.prereq = prereq

    def add(self, tasks):
        for task in tasks:
            if task in self.done:
                continue
            if len(self.queue) >= workers or not is_all_done(self.done, self.prereq[task]):
                if task not in self.wait_list:
                    self.wait_list.append(task)
            else:
                self._do_add(task)

    def _do_add(self, task):
        # add a tuple of task and time when finished
        for (time, qtask) in self.queue:
            if qtask == task:
                return
        work = ( self.timer + ord(task) - ord('A') + 1 + self.delay, task)
        self.queue.append(work)
        print("adding", work)

    def _do_work(self):
        self.queue.sort()
        task = self.queue.pop(0)
        if not (task[1] in self.done):
            self.timer = task[0]
            self.done.add(task[1])
            print("worked on", task[1], "time =", self.timer)

        if self.wait_list:
            for task in self.wait_list:
                if is_all_done(self.done, self.prereq[task]):
                    self.wait_list.remove(task)
                    self._do_add(task)
                    break

    def work(self):
        if self.queue:
            self._do_work()

    def finish(self):
        while self.queue:
            self._do_work()


steps_regex = re.compile("Step (\w).*step (\w)")

with open(INPUT) as f:
    data = [x.strip() for x in f.readlines()]

    # parse datas
    graph = defaultdict(list)
    prereq = defaultdict(list)
    origin = set()
    target = set()
    for line in data:
        re = steps_regex.match(line)
        f = re.group(1)
        t = re.group(2)
        origin.add(f)
        target.add(t)
        graph[f].append(t)
        prereq[t].append(f)

    # nodes that are not targets
    starter = origin - target

    # part 1
    available = list(starter)
    result = ""
    while len(available) > 0:
        available.sort()
        node = available.pop(0)
        if node in result:
            continue
        result += node
        togo = sorted(graph[node])
        for desc in togo:
            if is_all_done(result, prereq[desc]):
                available.append(desc)
    print(result)

    # part 2
    available = sorted(list(starter))
    result = ""
    f = Factory(workers, delay, prereq)
    f.add(available)
    while len(available) > 0:
        f.work()
        node = available.pop(0)
        togo = sorted(graph[node])
        f.add(togo)
        available.extend(togo)

    f.finish()

    print(f.timer)
