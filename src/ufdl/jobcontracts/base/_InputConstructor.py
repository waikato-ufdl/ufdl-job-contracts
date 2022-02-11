from typing import Dict, Union

from ufdl.jobtypes.base import UFDLJSONType, UFDLType

from ..params import TypeConstructor
from ._Input import Input


class InputConstructor:
    def __init__(self, *type_constructors: Union[UFDLType, TypeConstructor], help: str):
        for type_constructor in type_constructors:
            if isinstance(type_constructor, TypeConstructor):
                bound_base = type_constructor.bound_base
                if bound_base is not None and not bound_base.is_subtype_of(UFDLJSONType()):
                    raise ValueError(f"Input constructor is not guaranteed to construct a JSON-compatible type")
            elif isinstance(type_constructor, UFDLType):
                if not type_constructor.is_subtype_of(UFDLJSONType()):
                    raise ValueError(f"Input type must be a JSON-compatible type")
            else:
                raise ValueError("All input constructors must be type-constructors or types")

        self._name = ""
        self._type_constructors = type_constructors
        self._help = help

    @property
    def name(self):
        return self._name

    @property
    def type_constructors(self):
        return self._type_constructors

    @property
    def help(self):
        return self._help

    def construct(self, types: Dict[str, UFDLType]):
        return Input(
            self._name,
            *(
                input_constructor.construct(types) if isinstance(input_constructor, TypeConstructor)
                else input_constructor
                for input_constructor in self._type_constructors
            ),
            help=self._help
        )
