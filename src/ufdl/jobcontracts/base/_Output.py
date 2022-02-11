import builtins
from typing import Any, Generic

from ufdl.jobtypes.base import UFDLType, OutputType


class Output(Generic[OutputType]):
    def __init__(self, name: str, type: UFDLType[tuple, Any, OutputType], *, help: str):
        if not isinstance(type, UFDLType):
            raise ValueError(f"All output types must be UFDL types, received: ({builtins.type(type)}) {type}")

        self._name = name
        self._type = type
        self._help = help

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def help(self):
        return self._help
