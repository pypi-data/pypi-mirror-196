"""
I can show you the world
"""


def world(a):
    """Unbelievable sunrise, clearly a super serious function

    Args:
        a (_type_): _description_

    Raises:
        NotImplementedError: _description_

    Returns:
        _type_: _description_
    """
    if isinstance(a, str):
        return a + "world"
    else:
        raise NotImplementedError()
