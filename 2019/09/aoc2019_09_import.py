from __future__ import print_function
import pathlib
import sys
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))
from aoc import read_input_ints_separated
from aoc.intcode import single_run

INPUT = "aoc2019_09_input.txt"

data = read_input_ints_separated(INPUT)

print(single_run(data, 1))
print(single_run(data, 2))

