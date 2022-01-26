from abc import ABC
from typing import Dict, Tuple, Union

from ufdl.jobtypes import AnyUFDLType
from ufdl.jobtypes.base import UFDLJSONType
from ufdl.jobtypes.util import format_type_args_or_params, is_subtype, is_ufdl_type

from ..initialise import name_type_translate
from ..params import JobContractParamName, JobContractParams, TypeConstructor


class UFDLJobContract(ABC):
    """
    TODO
    """
    _params: JobContractParams

    def __init_subclass__(cls, **kwargs):
        params = kwargs.pop('params')
        inputs_constructors = params.pop('inputs')
        outputs_constructor = params.pop('outputs')

        if not isinstance(params, JobContractParams):
            raise TypeError(f"Expected {JobContractParams}, got {type(params)}")

        if not isinstance(inputs_constructors, dict):
            raise TypeError(f"Inputs to a job-contract should be a dictionary")

        for input_name, input_constructors in inputs_constructors.items():
            if not isinstance(input_name, str) or not input_name.isidentifier():
                raise ValueError("All input names must be valid identifiers")
            if not isinstance(input_constructors, tuple):
                raise ValueError("Input constructors should be a tuple")
            for input_constructor in input_constructors:
                if isinstance(input_constructor, TypeConstructor):
                    bound_base = input_constructor.bound_base
                    if bound_base is not None and not is_subtype(bound_base, UFDLJSONType):
                        raise ValueError(f"Input constructor for '{input_name}' is not guaranteed to construct a JSON-compatible type")
                elif is_ufdl_type(input_constructor):
                    if not is_subtype(input_constructor, UFDLJSONType):
                        raise ValueError(f"Input type for '{input_name}' must be a JSON-compatible type")
                else:
                    raise ValueError("All input constructors must be type-constructors or types")

        if not isinstance(outputs_constructor, dict):
            raise TypeError(f"Outputs to a job-contract should be a dictionary")

        for output_name, output_constructor in outputs_constructor.items():
            if not isinstance(output_name, str) or not output_name.isidentifier():
                raise ValueError("All output names must be valid identifiers")
            if not isinstance(output_constructor, TypeConstructor) and not is_ufdl_type(output_constructor):
                raise ValueError("All output constructors must be type-constructors or types")

        cls._params = params
        cls._inputs_constructors: Dict[str, Tuple[Union[TypeConstructor, AnyUFDLType], ...]] = inputs_constructors
        cls._outputs_constructors: Dict[str, Union[TypeConstructor, AnyUFDLType]] = outputs_constructor

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
            types: Dict[JobContractParamName, AnyUFDLType]
    ):
        inputs: Dict[str, Tuple[AnyUFDLType, ...]] = {
            input_name: tuple(
                input_constructor.construct(types) if isinstance(input_constructor, TypeConstructor)
                else input_constructor
                for input_constructor in input_constructors
            )
            for input_name, input_constructors in self._inputs_constructors.items()
        }

        outputs: Dict[str, AnyUFDLType] = {
            output_name: (
                output_constructor.construct(types) if isinstance(output_constructor, TypeConstructor)
                else output_constructor
            )
            for output_name, output_constructor in self._outputs_constructors.items()
        }

        self._inputs = inputs
        self._outputs = outputs
        self._types = types

    @property
    def inputs(self):
        return self._inputs

    @property
    def outputs(self):
        return self._outputs

    def __str__(self):
        name = name_type_translate(type(self))
        if name is None:
            raise TypeError(f"No name translation for {type(self)}")
        args = (
            self._types[param.name]
            for param in self._params
        )
        return f"{name}{format_type_args_or_params(*args)}"
