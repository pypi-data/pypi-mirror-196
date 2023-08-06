import pandas as pd
import numpy as np


def add(a, b):
    """This adds things, untyped potentially dangerous

    Args:
        a (_type_): _description_
        b (_type_): _description_

    Returns:
        _type_: _description_
    """
    return a + b


def sub(a: str, b: int):
    """
    This doesn't even sub wtf was I thinking

    :param a: _description_
    :type a: str
    :param b: _description_
    :type b: int
    :return: _description_
    :rtype: _type_
    """
    return a + str(b)


def my_pd(a):
    """returns a pd Series, it's quite serious

    Args:
        a (_type_): _description_

    Returns:
        _type_: _description_
    """
    return pd.Series(a)


def my_np(a):
    """Numpy? you mean not my py

    Args:
        a (something): useless description

    Returns:
        _type_: _description_
    """
    return np.array(a)
