"""Defines a base for creating volux modules through subclassing."""

from typing import Callable, Any
from ..types import NoParamFunc
from ..util import _empty_func


class VoluxModule:
    """Used to enforce a consistent base among modules, create subclasses using this."""

    def __init__(
        self,
        prepare: NoParamFunc,
        cleanup: NoParamFunc,
        supports_inputs: bool,
        supports_outputs: bool,
    ):
        """See class docstring."""
        # Module flags
        self.supports_inputs = supports_inputs
        self.supports_outputs = supports_outputs

        # Module context management
        self._prepare = prepare
        self._cleanup = cleanup

        # Module context management pre/post hooks
        # TODO(Denver): add support for pre/post-prepare/cleanup functions
        self._pre_prepare = _empty_func
        self._post_prepare = _empty_func
        self._pre_cleanup = _empty_func
        self._post_cleanup = _empty_func

    def __enter__(self) -> Any:
        """Call prepare method."""
        self.prepare()
        return self

    def __exit__(
        self, exception_type: Any, exception_value: Any, traceback: Any
    ) -> Any:
        """Call cleanup method."""
        return self.cleanup()

    def prepare(self) -> None:
        """Prepare the module for use."""
        self._pre_prepare()
        self._prepare()
        self._post_prepare()

    def cleanup(self) -> None:
        """Cleanup the module after use."""
        self._pre_cleanup()
        self._cleanup()
        self._post_cleanup()


class VoluxSource(VoluxModule):
    """Superclass for a volux module that doesn't accept inputs."""

    def __init__(self, prepare: NoParamFunc, cleanup: NoParamFunc) -> None:
        """See class docstring."""
        super().__init__(
            prepare=prepare,
            cleanup=cleanup,
            supports_inputs=False,
            supports_outputs=True,
        )


class VoluxTransformer(VoluxModule):
    """Superclass for a volux module that takes n inputs and returns n outputs."""

    def __init__(self, prepare: NoParamFunc, cleanup: NoParamFunc) -> None:
        """See class docstring."""
        super().__init__(
            prepare=prepare,
            cleanup=cleanup,
            supports_inputs=True,
            supports_outputs=True,
        )


class VoluxDestination(VoluxModule):
    """Superclass for a volux module that only takes inputs (can optionally pass through input values)."""

    def __init__(self, prepare: NoParamFunc, cleanup: NoParamFunc) -> None:
        """See class docstring."""
        super().__init__(
            prepare=prepare,
            cleanup=cleanup,
            supports_inputs=True,
            supports_outputs=False,
        )
