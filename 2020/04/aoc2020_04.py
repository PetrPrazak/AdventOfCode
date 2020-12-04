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
    cnt = 0
    for key in fields.keys():
        if key in passport:
            cnt += 1
    return cnt == len(fields)


def values_ok(passport):
    for key in fields.keys():
        value = passport[key]
        if not fields[key](value):
            return False
    return True


def process(data):
    valids = 0
    checked = 0
    for passport in data:
        valid = all_fields_are_present(passport)
        if valid:
            valids += 1
            if values_ok(passport):
                checked += 1

    print("part 1:", valids)
    print("part 2:", checked)


def parse_line(outdict, line):
    fields = line.split()
    for field in fields:
        key, value = field.split(':')
        outdict[key] = value


def load_data(lines):
    passwords = [dict()]
    idx = 0
    for line in lines:
        line = line.strip()
        if not line:
            passwords.append(dict())
            idx += 1
        else:
            parse_line(passwords[idx], line)
    return passwords


def main(file):
    print(file)
    with open(file) as f:
        process(load_data(f.readlines()))


if __name__ == "__main__":
    # main("test.txt")
    main("input.txt")
