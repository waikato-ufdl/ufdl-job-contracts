from typing import Generic

from ufdl.jobtypes.base import UFDLType

from ..params import TypeConstructor
from ._TypesType import TypesType


class Output(Generic[TypesType]):
    def __init__(self, type: TypesType, *, help: str):
        if not isinstance(type, TypeConstructor) and not isinstance(type, UFDLType):
            raise ValueError("All output constructors must be type-constructors or types")

        self._type = type
        self._help = help

    @property
    def type(self):
        return self._type

    @property
    def help(self):
        return self._help
