from typing import Dict, TypeVar, Union

from ufdl.jobtypes.base import UFDLType

from ..params import TypeConstructor
from ._Output import Output

OutputType = TypeVar('OutputType')


class OutputConstructor:
    def __init__(self, type_constructor: Union[UFDLType, TypeConstructor], *, help: str):
        if not isinstance(type_constructor, TypeConstructor) and not isinstance(type_constructor, UFDLType):
            raise ValueError("All output constructors must be type-constructors or types")

        self._name = ""
        self._type_constructor = type_constructor
        self._help = help

    @property
    def name(self):
        return self._name

    @property
    def type_constructor(self):
        return self._type_constructor

    @property
    def help(self):
        return self._help

    def construct(self, types: Dict[str, UFDLType]):
        type_constructor = self._type_constructor
        return Output(
            self._name,
            (
                type_constructor.construct(types) if isinstance(type_constructor, TypeConstructor)
                else type_constructor
            ),
            help=self._help
        )
