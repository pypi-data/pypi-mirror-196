
"""
Exceptions which can be raised by py-Puii Itself.
"""


class pyPuiiError(Exception):
    ...


class TelethonMissingError(ImportError):
    ...


class DependencyMissingError(ImportError):
    ...


class RunningAsFunctionLibError(pyPuiiError):
    ...
