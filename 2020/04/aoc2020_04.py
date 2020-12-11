# https://adventofcode.com/2020/day/4
from __future__ import print_function
import re


def byr_valid(value):
    num = int(value)
    return 1920 <= num <= 2002


def iyr_valid(value):
    num = int(value)
    return 2010 <= num <= 2020


def eyr_valid(value):
    num = int(value)
    return 2020 <= num <= 2030


def hgt_valid(value):
    num = int(value[:-2])
    unit = value[-2:]
    if unit == 'cm':
        return 150 <= num <= 193
    elif unit == 'in':
        return 59 <= num <= 76
    return False


hcl_re = re.compile('#[0-9a-f]{6}$')


def hcl_valid(value):
    return hcl_re.match(value) is not None


def ecl_valid(value):
    return value in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']


pid_re = re.compile('[0-9]{9}$')


def pid_valid(value):
    return pid_re.match(value) is not None


fields = {'byr': byr_valid, 'iyr': iyr_valid, 'eyr': eyr_valid, 'hgt': hgt_valid,
          'hcl': hcl_valid, 'ecl': ecl_valid, 'pid': pid_valid}


def all_fields_are_present(passport):
    return all(key in passport for key in fields.keys())


def values_ok(passport):
    return all(fields[key](passport[key]) for key in fields.keys())


def process(data):
    valid_passports = [p for p in data if all_fields_are_present(p)]
    print("Part 1:", len(valid_passports))
    correct_passports = sum(1 for p in valid_passports if values_ok(p))
    print("Part 2:", correct_passports)


def parse_line(line):
    return dict(field.split(":") for field in line.split())


def merge_lines(fileobj):
    """
    Joins the lines until the empty line or EOF
    """
    complete = []
    for line in fileobj:
        line = line.strip()
        if not line:
            yield ' '.join(complete)
            complete = []
        complete.append(line)
    if complete:
        yield ' '.join(complete)


def load_data(fileobj):
    return [parse_line(line) for line in merge_lines(fileobj)]


def main(file):
    print(file)
    with open(file) as f:
        process(load_data(f))


if __name__ == "__main__":
    # main("test.txt")
    main("input.txt")
