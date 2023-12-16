from dataclasses import dataclass
from typing import List

import numpy as np

from advent_of_code.commons.commons import read_input_to_list


@dataclass
class File:
    name: str
    size: int


class Directory:
    PAD_OFFSET = 4

    def __init__(self, name: str):
        self.name = name
        self.parent: "Directory" | None = None
        self.size: int | None = None
        self.sub_directories: List["Directory"] = []
        self.files: List[File] = []

    def get_parent(self):
        assert self.parent is not None
        return self.parent

    def add_dir(self, name):
        new_dir = Directory(name)
        new_dir.parent = self
        not_present_yet = True
        for d in self.sub_directories:
            if d.name == name:
                not_present_yet = False

        if not_present_yet:
            self.sub_directories.append(new_dir)

    def add_file(self, name: str, size: int):
        f = File(name, size)
        if f not in self.files:
            self.files.append(f)

    def cd_into(self, name):
        for d in self.sub_directories:
            if d.name == name:
                return d

        raise RuntimeError("dir not in sub-directory list")

    def compute_size(self) -> int:
        self.size = np.sum([d.compute_size() for d in self.sub_directories])
        self.size += np.sum([f.size for f in self.files])
        self.size = int(self.size)
        return self.size

    def dirs_with_max_size(self, max_size: int) -> List[int]:
        result = []
        for d in self.sub_directories:
            result.extend(d.dirs_with_max_size(max_size))

        if self.size <= max_size:
            result.append(self.size)

        return result

    def print(self, level: int = 0):
        offset = level * self.PAD_OFFSET
        s_offset = " " * offset
        print(f"{s_offset}- {self.name} (dir)")
        for d in self.sub_directories:
            d.print(level + 1)

        s_offset = " " * (offset + self.PAD_OFFSET)
        for f in self.files:
            print(f"{s_offset}- {f.name} (file, size={f.size})")

    def get_dir_sizes(self) -> List[int]:
        result = [self.size]
        for d in self.sub_directories:
            result.extend(d.get_dir_sizes())

        return result


def build_file_tree(lines: List[str]) -> Directory:
    root = None
    curr_dir = None
    for l in lines:
        if l.startswith("$"):
            l = l[1:]
            if "/" in l:
                if root is None:
                    root = Directory("/")
                curr_dir = root
            elif "cd .." in l:
                curr_dir = curr_dir.get_parent()
            elif "cd" in l:
                dir_name = l.replace("cd", "", 1).strip()
                curr_dir = curr_dir.cd_into(dir_name)
            elif "ls" in l:
                continue
            else:
                raise RuntimeError("unknown command")
        elif l.startswith("dir"):
            curr_dir.add_dir(l.replace("dir", "", 1).strip())

        elif l[0].isdigit():
            p = l.split()
            curr_dir.add_file(p[1].strip(), int(p[0].strip()))

        else:
            raise RuntimeError("unknown error")

    return root


def part_a(lines: List[str]) -> int:
    root = build_file_tree(lines)
    root.compute_size()
    sizes = root.dirs_with_max_size(100_000)

    return np.sum(sizes)


def part_b(lines: List[str]) -> int:
    root = build_file_tree(lines)
    root.compute_size()

    total_disk_space = 70000000
    min_unused_space = 30000000
    current_unsused_space = total_disk_space - root.size
    size_to_free_up = min_unused_space - current_unsused_space

    res = np.min([d for d in root.get_dir_sizes() if d > size_to_free_up])

    return res


def run() -> None:
    print("partA:")
    assert part_a(read_input_to_list(__file__)) == 1517599
    assert part_a(read_input_to_list(__file__, read_test_input=True)) == 95437

    print("partB:")
    assert part_b(read_input_to_list(__file__)) == 2481982
    assert part_b(read_input_to_list(__file__, read_test_input=True)) == 24933642

    print("done")
