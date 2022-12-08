# https://adventofcode.com/2022/day/7
from pathlib import Path

ROOT = "/"
PATH_SEP = "/"
UPDIR = ".."


def build_fs(data):
    cwd = root_dir = {}
    for line in data:
        line = line.rstrip()
        if line[0] == '$':  # command
            _, cmd, *args = line.split()
            if cmd == "cd":
                arg = args[0]
                cwd = root_dir if arg == ROOT else cwd[arg]
        else:
            size, name = line.split()
            cwd[name] = {UPDIR: cwd} if size == "dir" else int(size)
    return root_dir


def get_dir_sizes(name, a_dir):
    def _dir_size(name, a_dir):
        total = 0
        for entry, val in a_dir.items():
            if entry == UPDIR:
                continue
            if type(val) is dict:
                fname = name + (PATH_SEP if name[-1] != PATH_SEP else "") + entry
                total += _dir_size(fname, val)
            else:
                total += val
        sizes[name] = total
        return total
    sizes = {}
    _dir_size(name, a_dir)
    return sizes


def process(file_system):
    # part 1
    dirs = get_dir_sizes(ROOT, file_system)
    result = sum(s for s in dirs.values() if s <= 100000)
    print("part 1:", result)
    # part 2
    total_disk_space, required_space = 70000000, 30000000
    free_space = total_disk_space - dirs[ROOT]
    to_free = required_space - free_space
    result = min(s for s in dirs.values() if s >= to_free)
    print("part 2:", result)


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(build_fs(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
