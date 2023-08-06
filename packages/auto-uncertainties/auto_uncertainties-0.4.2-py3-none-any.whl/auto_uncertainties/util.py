# -*- coding: utf-8 -*-
from __future__ import annotations

import warnings
from functools import wraps

import numpy as np

from . import NumpyDowncastWarning


def ignore_runtime_warnings(f):
    """
    A decorator to ignore runtime warnings
    Parameters
    ----------
    f: function
        The wrapped function

    Returns
    -------
    wrapped_function: function
        The wrapped function
    """

    @wraps(f)
    def runtime_warn_inner(*args, **kwargs):
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("ignore", category=RuntimeWarning)
            response = f(*args, **kwargs)
        return response

    return runtime_warn_inner


def ignore_numpy_downcast_warnings(f):
    """
    A decorator to ignore NumpyDowncastWarning
    Parameters
    ----------
    f: function
        The wrapped function

    Returns
    -------
    wrapped_function: function
        The wrapped function
    """

    @wraps(f)
    def user_warn_inner(*args, **kwargs):
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("ignore", category=NumpyDowncastWarning)
            response = f(*args, **kwargs)
        return response

    return user_warn_inner


def is_iterable(y):
    try:
        iter(y)
    except TypeError:
        return False
    return True


def has_length(y):
    try:
        len(y)
    except TypeError:
        return False
    return True


def is_np_duck_array(cls):
    """Check if object is a numpy array-like, but not a Uncertainty

    Parameters
    ----------
    cls : class

    Returns
    -------
    bool
    """
    try:
        import numpy as np
    except ImportError:
        return False

    return issubclass(cls, np.ndarray) or (
        not hasattr(cls, "_nom")
        and not hasattr(cls, "_err")
        and hasattr(cls, "__array_function__")
        and hasattr(cls, "ndim")
        and hasattr(cls, "dtype")
    )


class Display(object):
    default_format: str = ""

    def _repr_html_(self):
        val_ = self._nom
        err_ = self._err
        if is_np_duck_array(type(self._nom)):
            header = "<table><tbody>"
            footer = "</tbody></table>"
            val = f"<tr><th>Magnitude</th><td style='text-align:left;'><pre>{val_}</pre></td></tr>"
            err = f"<tr><th>Error</th><td style='text-align:left;'><pre>{err_}</pre></td></tr>"
            return header + val + err + footer
        else:
            val = f"{val_}"
            err = f"{err_}"
            return f"{val} {chr(0x00B1)} {err}"

    def _repr_latex_(self):
        val_ = self._nom
        err_ = self._err
        if is_np_duck_array(type(self._nom)):
            s = (
                ", ".join(
                    [
                        f"{v} \\pm {e}"
                        for v, e in zip(val_.ravel(), err_.ravel())
                    ]
                )
                + "~"
            )
            header = "$"
            footer = "$"
            return header + s + footer
        else:
            val = f"{val_}"
            err = f"{err_}"
            return f"${val} \\pm {err}$"

    def __str__(self) -> str:
        val_ = self._nom
        err_ = self._err

        if self._nom is not None:
            if self._err is not None:
                if is_np_duck_array(type(self._nom)):
                    return (
                        "["
                        + ", ".join(
                            [
                                f"{v} +/- {e}"
                                for v, e in zip(val_.ravel(), err_.ravel())
                            ]
                        )
                        + "]"
                    )
                else:
                    return f"{val_} +/- {err_}"
            else:
                return f"{val_}"

    def __format__(self, fmt):
        val_ = self._nom
        err_ = self._err
        str_rep = f"{val_:{fmt}} +/- {err_:{fmt}}"
        return str_rep

    def __repr__(self) -> str:
        return str(self)


def strip_device_array(value):
    return np.array(value)


def ndarray_to_scalar(value):
    return np.ndarray.item(strip_device_array(value))
