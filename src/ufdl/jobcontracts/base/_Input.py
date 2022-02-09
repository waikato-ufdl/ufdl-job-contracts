from typing import Generic

from ufdl.jobtypes.base import UFDLJSONType, UFDLType

from ..params import TypeConstructor
from ._TypesType import TypesType


class Input(Generic[TypesType]):
    def __init__(self, *types: TypesType, help: str):
        for input_type in types:
            if isinstance(input_type, TypeConstructor):
                bound_base = input_type.bound_base
                if bound_base is not None and not bound_base.is_subtype_of(UFDLJSONType()):
                    raise ValueError(f"Input constructor is not guaranteed to construct a JSON-compatible type")
            elif isinstance(input_type, UFDLType):
                if not input_type.is_subtype_of(UFDLJSONType()):
                    raise ValueError(f"Input type must be a JSON-compatible type")
            else:
                raise ValueError("All input constructors must be type-constructors or types")

        self._name = ""
        self._types = types
        self._help = help

    @property
    def name(self):
        return self._name

    @property
    def types(self):
        return self._types

    @property
    def help(self):
        return self._help
