from typing import Generic

from ufdl.jobtypes.base import UFDLJSONType
from ufdl.jobtypes.util import is_subtype, is_ufdl_type

from ..params import TypeConstructor
from ._TypesType import TypesType


class Input(Generic[TypesType]):
    def __init__(self, *types: TypesType, help: str):
        for input_type in types:
            if isinstance(input_type, TypeConstructor):
                bound_base = input_type.bound_base
                if bound_base is not None and not is_subtype(bound_base, UFDLJSONType):
                    raise ValueError(f"Input constructor is not guaranteed to construct a JSON-compatible type")
            elif is_ufdl_type(input_type):
                if not is_subtype(input_type, UFDLJSONType):
                    raise ValueError(f"Input type must be a JSON-compatible type")
            else:
                raise ValueError("All input constructors must be type-constructors or types")

        self._types = types
        self._help = help

    @property
    def types(self):
        return self._types

    @property
    def help(self):
        return self._help
