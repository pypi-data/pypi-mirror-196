"""Defines various custom exceptions."""


class LinuxKernelModuleNotLoaded(OSError):
    """Exception thrown when a required linux kernel module has not been loaded."""


class DuplicateKeyError(ValueError):
    """Raised when an array contains multiple of the same string."""
