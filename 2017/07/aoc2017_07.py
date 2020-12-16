# http://adventofcode.com/2017/day/7
from __future__ import print_function
from collections import Counter


def solve(lines):
    # build the tree
    tree = dict()
    rootname = None
    for line in lines:
        parts = line.strip().split(" ")
        name = parts[0]
        subs = []
        if len(parts) > 2:
            subs = [x.strip(",") for x in parts[3:]]
            # set parent to children' node
            for s in subs:
                if s in tree:
                    data = tree[s]
                    tree[s] = (data[0], name, data[2])
                else:
                    tree[s] = (0, name, [])

        weight = int(parts[1][1:-1])
        parent = None
        if name in tree:
            parent = tree[name][1]
        else:
            rootname = name
        # set the node
        tree[name] = (weight, parent, subs)

    print("Root:", rootname)

    # find misbalanced node
    tree_weight(tree, name)


def tree_weight(tree, key):
    weight = tree[key][0]
    subs = tree[key][2]
    if not subs:
        return weight

    weights = [tree_weight(tree, k) for k in subs]
    cnt = Counter(weights)
    nums = cnt.most_common(2)
    if len(subs) != cnt[nums[0][0]]:
        diff = nums[0][0] - nums[1][0]
        idx = weights.index(nums[1][0])
        child = subs[idx]
        childweight = tree[child][0]
        print("Misbalanced node:", child, tree[child])
        print("Should weight:", childweight + diff)

    return weight + sum(weights)


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = f.readlines()
        solve(lines)
