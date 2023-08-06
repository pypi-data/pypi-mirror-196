from typing import Callable, Any, NamedTuple

NoParamFunc = Callable[[], Any]

# TODO: add docstring
class HSBK(NamedTuple):
    hue: int
    saturation: int
    brightness: int
    kelvin: int
