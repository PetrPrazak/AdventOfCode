# https://adventofcode.com/2020/day/16
from __future__ import print_function
from collections import defaultdict
from math import prod


def valid_field(fields, value):
    for ranges in fields.values():
        if any(value in range(*r) for r in ranges):
            return True
    return False


def validate_tickets(fields, tickets):
    return sum(x for t in tickets
               for x in t if not valid_field(fields, x))


def valid_ticket(fields, ticket):
    return all(valid_field(fields, val) for val in ticket)


def valid_tickets(fields, tickets):
    return filter(lambda t: valid_ticket(fields, t), tickets)


def valid_fields(fields, val):
    return [name for name, ranges in fields.items()
            for r in ranges if val in range(*r)]


def scan_fields(fields, tickets):
    # 1. find the fields valid for every value in ticket
    # and count every successful check for every field
    fields_order = defaultdict(lambda: defaultdict(int))
    for t in valid_tickets(fields, tickets):
        for i, val in enumerate(t):
            for name in valid_fields(fields, val):
                fields_order[name][i] += 1

    # 2. keep only indices with max value
    for field, counters in fields_order.items():
        maxx = max(counters.values())
        fields_order[field] = {idx for idx, num in counters.items()
                               if num == maxx}

    # 3. eliminate gradually all used indices
    # from the smallest set to the biggest
    used = set()
    field_indices = dict()
    for name, idx in sorted(fields_order.items(), key=lambda el: len(el[1])):
        uniq = idx - used
        assert len(uniq) == 1
        field_indices[name] = uniq.pop()
        used.update(idx)

    return field_indices


def process(data):
    # part 1
    fields, myticket, tickets = data
    result = validate_tickets(fields, tickets)
    print("part 1:", result)
    # part 2
    indices = scan_fields(fields, tickets)
    result = prod(myticket[i] for name, i in indices.items()
                  if name.startswith('departure'))
    print("part 2:", result)


def parse_fields(lines):
    fields = dict()
    for l in lines.split("\n"):
        name, ranges = l.split(": ")
        rng = [r.split("-") for r in ranges.split(" or ")]
        fields[name] = [(int(s), int(e) + 1) for s, e in rng]
    return fields


def parse_tickets(lines):
    _, *data = lines.split("\n")
    return [[int(f) for f in l.strip().split(",")] for l in data]


def load_data(fileobj):
    fields, your_data, tickets = fileobj.read().split("\n\n")
    return parse_fields(fields), parse_tickets(your_data)[0], parse_tickets(tickets)


def main(file):
    print(file)
    with open(file) as f:
        process(load_data(f))


if __name__ == "__main__":
    main("test.txt")
    main("input.txt")
