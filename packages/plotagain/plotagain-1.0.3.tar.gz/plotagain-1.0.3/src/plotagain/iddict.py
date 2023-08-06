from collections.abc import MutableMapping
from typing import Any, Dict, Optional, Iterable, Iterator


class IDDict(MutableMapping):
    """
    A dict which accepts any object as a key. Uses the id of the object as the hash

    Attributes
    ----------
    id_keyed_keys
        A dict mapping the id of all the keys to the keys themselves
    id_keyed_values
        A dict mapping the id of all the keys to the corresponding values
    """
    id_keyed_keys: Dict[int, Any]
    id_keyed_values: Dict[int, Any]

    def __init__(self, dict_: Optional[Dict[Any, Any]] = None):
        """
        Initializes id_keyed_keys and id_keyed_values with the content of dict_ if provided

        Parameters
        ----------
        dict_
        """
        super().__init__()
        self.id_keyed_keys = {}
        self.id_keyed_values = {}

        if dict_:
            for k, v in dict_.items():
                self[k] = v

    def __len__(self) -> int:
        return len(self.id_keyed_keys)

    def __iter__(self) -> Iterator:
        return iter(self.id_keyed_keys.values())

    def __delitem__(self, key: Any) -> None:
        del self.id_keyed_keys[id(key)]
        del self.id_keyed_values[id(key)]

    def __getitem__(self, item) -> Any:
        return self.id_keyed_values[id(item)]

    def __contains__(self, item) -> bool:
        return id(item) in self.id_keyed_values

    def __setitem__(self, key, value) -> None:
        self.id_keyed_keys[id(key)] = key
        self.id_keyed_values[id(key)] = value

    def keys(self) -> Iterable[Any]:
        return self.id_keyed_keys.values()

    def items(self) -> Iterable[Any]:
        return ((k, self[k]) for k in self.keys())

    def update(self, dict_: MutableMapping, reverse: bool = False) -> None:
        """
        Updates the content of the IDDict with the contents of dict_. If reverse=True, the values and keys are swapped

        Parameters
        ----------
        dict_
            A dict used to update the contents of this instance
        reverse
            Whether to swap the keys and values of dict_
        """
        for k, v in dict_.items():
            if reverse:
                k, v = v, k
            self[k] = v

    @property
    def reverse(self) -> "IDDict":
        """
        Returns a copy of this instance with the keys and values switched

        Returns
        -------
        IDDict
        """
        reverse = IDDict()
        for k, v in self.items():
            reverse[v] = k
        return reverse
