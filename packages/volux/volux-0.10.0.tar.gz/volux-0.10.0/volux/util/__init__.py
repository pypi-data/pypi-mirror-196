"""Defines various utilities."""

# built-in
from typing import Any, Callable, List, Dict, Union
from functools import reduce

# site
import numpy as np

# local
from . import linux
from ..exceptions import DuplicateKeyError


def _empty_func() -> None:
    pass


class ResolveCallableParams:
    """Wrapper to call all callable params before calling the wrapped function."""

    def __init__(self) -> None:
        """See class docstring."""
        pass

    def __call__(self, func: Callable[..., Any]) -> Any:
        """Call all callable parameters before calling wrapped function with params."""

        def _paramStrippedFunc(*args: Any, **kwargs: Any) -> Any:
            arg_list = list(args)
            for i in range(len(arg_list)):
                arg_n = arg_list[i]
                arg_callable = callable(arg_n)
                if arg_callable:
                    arg_list[i] = arg_list[i]()

            args = tuple(arg_list)

            # TODO(Denver): add support for resolving kwargs

            return func(*args, **kwargs)

        return _paramStrippedFunc


# TODO(Denver): write tests for has_duplicates
def has_duplicates(str_list: List[str]) -> bool:
    """Check if given list contains any duplicates values."""
    return False if len(str_list) == len(set(str_list)) else True


# TODO(Denver): write tests for recursive_split
def recursive_split(
    data: Union[str, List[Union[str, Any]]], sep: str
) -> Union[str, List[Union[str, Any]]]:
    """Split strings in an n-dimensional array recursively by separator."""
    if isinstance(data, list):
        return [recursive_split(item, sep) for item in data]
    if isinstance(data, str):
        # if sep found in data, return a split version, otherwise return unchanged
        # ... (splitting data by a seperator that the data doesn't contain will
        # ... return the data in an array; for our purposes, we want to avoid this)
        return data.split(sep) if sep in data else data
    raise TypeError("expected data to be a list or string")


# TODO(Denver): write tests for dictify_arrays
def dictify_arrays(
    cls,
    keys: List[str],
    data_rows: List[List[str]],
    lowercase_keys=False,
    seps: List[str] = [],
) -> List[Dict[str, str]]:
    """Turn a list of keys and a 2D list of values into an list of dicts.

    For example, consider this scenario:

    Input: `
        dictify_arrays(
            ['Module','Size','Used','By'],
            [
                ['v4l2loopback','45056'],
                ['nf_nat_ipv4', '16384', '2', 'ipt_MASQUERADE,nft_chain_nat_ipv4']
            ],
            lowercase_keys=True,
            seps=[',']
        )
    `

    Output: `
        [
            {
                'module': 'v4l2loopback',
                'size': '45056'
            },
            {
                'module': 'nf_nat_ipv4'
                'size': '16384'
                'used': '2'
                'by': [
                    'ipt_MASQUERADE',
                    'nft_chain_nat_ipv4'
                ]
            }
        ]
    `

    :param keys: List of strings to be used as dict keys in corresponding data column indices.
    :type keys: List[str]
    :param data_rows: 2D array of data by rows and columns
    :type data_rows: List[List[str]]
    :param lowercase_keys: Specify if all keys should be transformed to lowercase, defaults to False
    :type lowercase_keys: bool, optional
    :param seps: List of separators to recursively split keypair values into lists, defaults to []
    :type seps: List[str], optional
    :raises DuplicateKeyError: A string was found in the keys list multiple times
    :return: List of dictionaries representing each row
    :rtype: List[Dict[str, str]]
    """
    if lowercase_keys:
        keys = [key.lower() for key in keys]

    if has_duplicates(keys):
        raise DuplicateKeyError(
            "Duplicates key strings found in list",
            keys,
            {"lowercase_keys": lowercase_keys},
        )

    list_of_row_dicts = []
    for row_idx in range(len(data_rows)):
        row_list = data_rows[row_idx]
        row_dict = {
            keys[col_idx]: reduce(recursive_split, seps, row_list[col_idx])
            for col_idx in range(len(row_list))
        }
        list_of_row_dicts.append(row_dict)

    return list_of_row_dicts


# TODO: improve docstring
def mapped(n, start1, stop1, start2, stop2):
    """Remap range of value n from start1..stop2 to start2..stop2."""
    return ((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2


# TODO: add docstring
def clamp(n: float, minimum: float, maximum: float) -> float:
    return min(max(minimum, n), maximum)


# TODO: improve docstring
def exponentialize(n):
    """Convert a number between range 0..1 to an exponential form.

    It's expected the input values are linear in nature.
    """
    exponential_max = n**2
    return np.sqrt(n) * exponential_max


# TODO: improve docstring
class Strobify:
    """
    Strobe a value provided by internally incrementing a frame counter on each call.

    Calling instance returns e during frames_on period, else returns strobe_e until frames_off period ends.

    Frame counter resets to 0 after frames_off period ends.

    WARNING: stateful and side-effects very possible.
    """

    def __init__(self, frames_on, frames_off, strobe_e):
        """See class docstring."""
        self.on_until_f = frames_on - 1
        self.off_until_f = self.on_until_f + frames_off
        self.f = -1
        self.strobe_e = strobe_e

    def __call__(self, e):
        self._next_frame()

        if self.f <= self.on_until_f:
            return e
        elif self.f <= self.off_until_f:
            return self.strobe_e

    def _next_frame(self):
        self.f = self.f + 1

        if self.f > self.off_until_f:
            self.f = 0


# TODO: improve docstring
class TimedThresholdGate:
    """
    Gate that only opens after n many seconds above a given threshold.

    `.is_open()` must be called at least once per frame (and no more) at a regular interval for an accurate output.
    """

    def __init__(self, energy_threshold, time_threshold_in_seconds, fps):
        self.counter = 0
        # must exceed this amount for given time
        self.energy_threshold = energy_threshold
        # must exceed energy threshold for at least this many frames
        self.consecutive_frame_threshold = time_threshold_in_seconds * fps
        # how many frames the gate has been open for
        self.open_counter = 0

    def is_open(self, e):
        """
        Returns boolean indicating if gate is open.

        WARNING: Stateful - intentional side-effects on call
        """

        if e >= self.energy_threshold:
            self.counter += 1
            if self.counter >= self.consecutive_frame_threshold:
                self.open_counter += 1
                return True
        else:
            self.counter = 0
            self.open_counter = 0
        return False

    def get_time_threshold_ratio(self):
        return min(
            (self.counter / self.consecutive_frame_threshold),
            1,
        )
