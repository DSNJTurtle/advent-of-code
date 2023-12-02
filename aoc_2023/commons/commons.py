import os
from pathlib import Path
from typing import List


def read_input_to_list(file: str, read_test_input: bool = False) -> List[str]:
    """Read input

    Args:
        file: Filepath to caller
        read_test_input: Read "test.txt" instead of "input.txt" if true. Defaults to False.

    Returns:
        List of strings per line in the file.
    """
    f = "test.txt" if read_test_input else "input.txt"
    filepath = os.path.join(Path(file).parent, f)
    with open(filepath, "r") as f:
        return [x.rstrip("\n") for x in f.readlines()]
