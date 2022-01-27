from typing import Generic, Union

from ufdl.jobtypes.util import AnyUFDLType, is_ufdl_type

from ..params import TypeConstructor
from ._TypesType import TypesType


class Output(Generic[TypesType]):
    def __init__(self, type: TypesType, *, help: str):
        if not isinstance(type, TypeConstructor) and not is_ufdl_type(type):
            raise ValueError("All output constructors must be type-constructors or types")

        self._type = type
        self._help = help

    @property
    def type(self):
        return self._type

    @property
    def help(self):
        return self._help
