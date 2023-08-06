from typing import Any, Dict, List, Optional, Tuple, Type, TypeVar, Union


class _Inspect:
    """Inspired by `rich`

    https://github.com/Textualize/rich/blob/0f693f5c3d5f4f600751d244d1b95570106064bf/rich/_inspect.py
    """

    def __init__(self, obj: Any) -> None:
        self._obj = obj

    @property
    def attributes(self):
        return {k: v for k, v in vars(self._obj).items() if not k.startswith("_")}

    @property
    def privates(self):
        return {
            k: getattr(self._obj, k)
            for k in dir(self._obj)
            if k.startswith("_") and not k.startswith("__")
        }

    @property
    def dunders(self):
        return {k: getattr(self._obj, k) for k in dir(self._obj) if k.startswith("__")}
