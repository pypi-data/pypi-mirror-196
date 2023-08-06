"""Utilities relevant to Linux specifically."""

import subprocess
from collections import namedtuple
from typing import List

KernelModule = namedtuple(
    "KernelModule", ["name", "size", "used_by_count", "used_by_names"]
)


def loaded_modules() -> List[KernelModule]:
    """Returns a list of loaded kernel modules.

    :return: List of loaded kernel modules
    :rtype: List[KernelModule]
    """
    lsmod_proc = subprocess.Popen(["lsmod"], stdout=subprocess.PIPE)
    stdout, strerr = lsmod_proc.communicate()
    lines = [line.split() for line in stdout.decode("utf-8").splitlines()]
    module_lines = lines[1:]
    modules = [
        KernelModule(
            module_data[0],
            module_data[1],
            module_data[2],
            module_data[3] if len(module_data) >= 4 else [],
        )
        for module_data in module_lines
    ]
    return modules


__all__ = ["loaded_modules"]
