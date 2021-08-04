"""
Defines miscellaneous mathematical utility functions
"""


def positive_int(n: any) -> int:
    """
    Tries to convert a variable to a positive integer and raises an exception
    if it fails
    """
    n = int(n)
    if n < 0:
        raise ValueError('"n" must be non-negative')
    return n


def limit(value, bottom, top):
    return min(top, max(bottom, value))
