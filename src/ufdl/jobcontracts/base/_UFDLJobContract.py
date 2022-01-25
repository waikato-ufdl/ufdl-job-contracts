from abc import ABC
from typing import Dict, Tuple

from ufdl.jobtypes import AnyUFDLType
from ufdl.jobtypes.base import UFDLJSONType, UFDLType
from ufdl.jobtypes.util import format_type_args_or_params

from ..initialise import name_type_translate
from ..params import JobContractParamName, JobContractParams


class UFDLJobContract(ABC):
    """
    TODO
    """
    _params: JobContractParams

    def __init_subclass__(cls, **kwargs):
        params = kwargs.pop('params')

        if not isinstance(params, JobContractParams):
            raise TypeError(f"Expected {JobContractParams}, got {type(params)}")

        cls._params = params

    @classmethod
    def params(cls):
        return cls._params

    @classmethod
    def format(cls):
        name = name_type_translate(cls)
        if name is None:
            raise TypeError(f"No name translation for {cls}")
        return f"{name}{cls._params}"

    def __init__(
            self,
            inputs: Dict[str, Tuple[UFDLJSONType, ...]],
            outputs: Dict[str, UFDLType]
    ):
        # Check the inputs
        for input_name, input_type in inputs.items():
            if not input_name.isidentifier():
                raise ValueError(f"Input name '{input_name}' is not an identifier")
            if not isinstance(input_type, UFDLJSONType):
                raise ValueError(f"Input type for input '{input_name}' is not a JSON type ({type(input_type)})")

        # Check the outputs
        for output_name, output_type in outputs.items():
            if not output_name.isidentifier():
                raise ValueError(f"Output name '{output_name}' is not an identifier")
            if not isinstance(output_type, UFDLType):
                raise ValueError(f"Output type for output '{output_name}' is not a binary type ({type(output_type)})")

        self._inputs = inputs
        self._outputs = outputs
        self._types: Dict[JobContractParamName, AnyUFDLType] = {}

    @property
    def inputs(self):
        return self._inputs

    @property
    def outputs(self):
        return self._outputs

    def _set_types(self, types: Dict[JobContractParamName, AnyUFDLType]):
        self._types = types

    def __str__(self):
        name = name_type_translate(type(self))
        if name is None:
            raise TypeError(f"No name translation for {type(self)}")
        args = (
            self._types[param.name]
            for param in self._params
        )
        return f"{name}{format_type_args_or_params(*args)}"
