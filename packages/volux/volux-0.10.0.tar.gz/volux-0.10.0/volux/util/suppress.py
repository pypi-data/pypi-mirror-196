"""Define a context manager to suppress stdout and stderr."""

import os
from typing import Any


# full credit goes to jeremiahbuddha from StackOverflow for writing the original version of this context manager:
# ... https://stackoverflow.com/questions/11130156/suppress-stdout-stderr-print-from-python-functions


class SuppressStdoutStderr:
    """Context manager that will suppress all stdout and stderr, even if the stdout/stderr originates from compiled functions.

    This will not suppress raised exceptions.
    """

    def __init__(self) -> None:
        """See class docstring."""
        # Open a pair of null files
        self.null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = [os.dup(1), os.dup(2)]

    def __enter__(self) -> None:
        """Assign null pointers to stdout and stderr."""
        os.dup2(self.null_fds[0], 1)
        os.dup2(self.null_fds[1], 2)

    def __exit__(self, *_: Any) -> None:
        """Re-assign real stdout/stderr back to (1) and (2)."""
        os.dup2(self.save_fds[0], 1)
        os.dup2(self.save_fds[1], 2)
        # Close all file descriptors
        for fd in self.null_fds + self.save_fds:
            os.close(fd)
