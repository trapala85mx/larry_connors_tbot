# Python
import functools
from typing import List
# Project
from utils.errors.class_errors import ArgumentsMissingError
# Externals


def validate_class(args):
    def decorator(cls):
        @functools.wraps(cls)
        def wrapper(**kwargs):
            for a in args:
                if not a in kwargs.keys():
                    raise ArgumentsMissingError(a)
            return cls(**kwargs)
        return wrapper
    return decorator