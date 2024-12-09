from __future__ import annotations

import os
from dataclasses import is_dataclass
from pathlib import Path
from typing import Any, Callable, List


def read_input_to_list(file: str, filename: str | None = None, read_test_input: bool = False) -> List[str]:
    """
    Read input.

    Args:
        file: Filepath to caller
        filename: File to read
        read_test_input: Read "test.txt" instead of "input.txt" if true. Defaults to False.

    Returns:
        List of strings per line in the file.

    """
    f = filename if filename is not None else "test.txt" if read_test_input else "input.txt"
    filepath = os.path.join(Path(file).parent, f)
    with open(filepath, "r") as f:
        return [x.rstrip("\n") for x in f.readlines()]


class Node:
    """General node that accepts any dataclass data object."""

    def __init__(self, data):
        assert is_dataclass(data)
        self.data = data
        self.prev: Node | None = None
        self.next: Node | None = None


class DoublyLinkedList:
    """General doubly linked list."""

    def __init__(self):
        self.head: Node | None = None
        self.tail: Node | None = None
        self.size = 0

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
            new_node.prev = current

        self.tail = new_node
        self.size += 1

    def remove(self, data, search_func: Callable[[Any, Any], bool]):
        """
        Find node and remove it from the list.

        Args:
            data: Data attributes to filter by.
            search_func: 1st order funtion that compares data objects.

        Returns: None

        """
        current = self.head
        while current:
            if search_func(current.data, data):
                if current.prev:
                    current.prev.next = current.next
                else:
                    # we must be at head position if no prev element is present
                    self.head = current.next

                if current.next:
                    current.next.prev = current.prev
                else:
                    # we must be at tail position if no next element is present
                    self.tail = current.prev

                self.size -= 1
                return  # Node found and removed

            current = current.next

    def search(self, data, search_func: Callable[[Any, Any], bool]) -> Node | None:
        """
        Find a node by given search function.

        Args:
            data: Data attributes to filter by.
            search_func: 1st order funtion that compares data objects.

        Returns: Returns found node if present. Otherwise None

        """
        current = self.head
        while current:
            if search_func(current.data, data):
                return current
            current = current.next

        return None

    def reduce_left(self, reduce_func: Callable, initial=None):
        """
        Applies a function to the elements of the linked list from left to right, accumulating a result.

        Args:
            reduce_func: A function that takes two arguments, first argument is the accumulated result and second
            argument is the new input, and returns a single result.
            initial: The initial value for the accumulation (default is None).

        Returns: The accumulated result.

        """
        current = self.head
        result = initial
        while current:
            result = reduce_func(result, current.data)
            current = current.next

        return result

    def __str__(self):
        s = ""
        current = self.head
        while current:
            s += str(current.data) + " <-> "
            current = current.next

        s += "None"
        return s

    def display(self):
        print(str(self))

    def replace_data(self, orig_data, new_data) -> bool:
        """
        Finds first node in list containing orig_data and replaces the data by new_data.

        Args:
            orig_data: Original data of node.
            new_data: New data of node.

        Returns: True, if node was found and data replaced. False otherwise.

        """
        current = self.head
        while current:
            if current.data == orig_data:
                current.data = new_data
                return True
            current = current.next

        return False
