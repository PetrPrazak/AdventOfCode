# https://adventofcode.com/2022/day/7
from pathlib import Path


def build_fs(data):
    cwd = FS = {}
    for line in data:
        line = line.rstrip()
        if line[0] == '$':  # command
            _, cmd, *args = line.split()
            if cmd == "cd":
                arg = args[0]
                cwd = FS if arg == '/' else cwd[arg]
        else:
            size, name = line.split()
            cwd[name] = {"..": cwd} if size == "dir" else int(size)
    return FS


def get_dir_sizes(name, a_dir):
    def _dir_size(name, a_dir):
        if name in sizes:
            return sizes[name]
        total = 0
        for entry, val in a_dir.items():
            if entry == "..":
                continue
            if type(val) == dict:
                fname = name + ("/" if name[-1] != "/" else "") + entry
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
    dirs = get_dir_sizes("/", file_system)
    result = sum(s for s in dirs.values() if s <= 100000)
    print("part 1:", result)
    # part 2
    total_disk_space, required_space = 70000000, 30000000
    free_space = total_disk_space - dirs["/"]
    to_free = required_space - free_space
    result = sorted(s for s in dirs.values() if s >= to_free)[0]
    print("part 2:", result)


def main(file="input.txt"):
    print(file)
    with Path(__file__).parent.joinpath(file).open() as f:
        process(build_fs(f))


if __name__ == "__main__":
    # main("test.txt")
    main()
