import pickle
from pathlib import Path
from typing import Any, MutableMapping, Union

primitives = (int, str, bool, float)


def is_primitive(obj: Any) -> bool:
    """
    Returns whether the given object is a subclass of one of the 4 python primitive types: int, str, bool, float. Since
    numpy numbers subclass the primitives, these are included in the definition

    Parameters
    ----------
    obj
        An object the type of which to check

    Returns
    -------
    bool
        Whether or not obj is a primitive type
    """
    return any(isinstance(obj, primitive) for primitive in primitives)


def insert_next_available(dict_: MutableMapping, key: str, val: Any) -> str:
    """
    Inserts val into dict_ with the given key if the key does not already exist in dict_. If key is already set in
    dict_, postfixes key with the smallest integer > 1 for which the post-fixed key is not in dict_

    Parameters
    ----------
    dict_
        The dict to insert the key/value into
    key
        The base key for insertion
    val
        The value to insert

    Returns
    -------
    str
        The final key used for insertion
    """
    postfix = ''
    ind = 1
    while key + postfix in dict_:
        ind += 1
        postfix = str(ind)

    dict_[key + postfix] = val
    return key + postfix


def load_pickle(filename: Union[str, Path]) -> Any:
    """
    Opens the given pickle file and returns the pickeled object

    Parameters
    ----------
    filename
        A path to a pickle file

    Returns
    -------
    Any
        The pickeled object
    """
    with open(filename, 'rb') as f:
        return pickle.load(f)


def write_pickle(filename: Union[str, Path], obj: Any) -> None:
    """
    Pickels the given obj to the given file

    Parameters
    ----------
    filename
        A path to a pickle file
    """
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)
