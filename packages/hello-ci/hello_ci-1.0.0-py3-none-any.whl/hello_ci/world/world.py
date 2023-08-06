"""
I can show you the world
"""


def world(a):
    """Unbelievable sunrise, clearly a super serious function

    :param a: _description_
    :type a: _type_
    :raises NotImplementedError: _description_
    :return: _description_
    :rtype: _type_
    """

    if isinstance(a, str):
        return a + "world"
    else:
        raise NotImplementedError()
