from typing import Any, Generic

from ufdl.jobtypes.base import UFDLJSONType, UFDLType, InputType


class Input(Generic[InputType]):
    def __init__(self, name: str, *types: UFDLJSONType[tuple, InputType, Any], help: str):
        for input_type in types:
            if not isinstance(input_type, UFDLType) or not input_type.is_subtype_of(UFDLJSONType()):
                raise ValueError(
                    f"All input types must be JSON-compatible UFDL types, received: "
                    f"({type(input_type)}) {input_type}"
                )

        self._name = name
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
