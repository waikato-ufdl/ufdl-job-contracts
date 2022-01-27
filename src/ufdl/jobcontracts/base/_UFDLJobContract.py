from abc import ABC
from typing import Dict, Union

from ufdl.jobtypes.util import format_type_args_or_params, AnyUFDLType

from . import Output
from ..initialise import name_type_translate
from ..params import JobContractParamName, JobContractParams, TypeConstructor
from ._Input import Input


class UFDLJobContract(ABC):
    """
    TODO
    """
    _params: JobContractParams

    def __init_subclass__(cls, **kwargs):
        params = kwargs.pop('params')
        input_constructors = kwargs.pop('inputs')
        output_constructors = kwargs.pop('outputs')

        if not isinstance(params, JobContractParams):
            raise TypeError(f"Expected {JobContractParams}, got {type(params)}")

        if not isinstance(input_constructors, dict):
            raise TypeError(f"Inputs to a job-contract should be a dictionary")

        for input_name, input_constructor in input_constructors.items():
            if not isinstance(input_name, str) or not input_name.isidentifier():
                raise ValueError("All input names must be valid identifiers")
            if not isinstance(input_constructor, Input):
                raise ValueError(f"Input '{input_name}' is not an {Input.__name__}")

        if not isinstance(output_constructors, dict):
            raise TypeError(f"Outputs to a job-contract should be a dictionary")

        for output_name, output_constructor in output_constructors.items():
            if not isinstance(output_name, str) or not output_name.isidentifier():
                raise ValueError("All output names must be valid identifiers")
            if not isinstance(output_constructor, Output):
                raise ValueError(f"Output '{output_name}' is not an {Output.__name__}")

        cls._params = params
        cls._inputs_constructors: Dict[str, Input[Union[TypeConstructor, AnyUFDLType]]] = input_constructors
        cls._outputs_constructors: Dict[str, Output[Union[TypeConstructor, AnyUFDLType]]] = output_constructors

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
        # Attempting to fix all bounds will check for type correctness
        self.params().get_new_bounds_for_fixed(**{
            str(name): type
            for name, type in types.items()
        })

        inputs: Dict[str, Input[AnyUFDLType]] = {
            input_name: Input(
                *(
                    input_constructor.construct(types) if isinstance(input_constructor, TypeConstructor)
                    else input_constructor
                    for input_constructor in input_constructors.types
                ),
                help=input_constructors.help
            )
            for input_name, input_constructors in self._inputs_constructors.items()
        }

        outputs: Dict[str, Output[AnyUFDLType]] = {
            output_name: Output(
                (
                    output_constructor.type.construct(types) if isinstance(output_constructor.type, TypeConstructor)
                    else output_constructor.type
                ),
                help=output_constructor.help
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
