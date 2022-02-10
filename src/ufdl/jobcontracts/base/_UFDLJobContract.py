from abc import ABC
from typing import Dict, Union

from ufdl.jobtypes.base import UFDLType

from . import Output
from ..initialise import name_type_translate
from ..params import JobContractParams, TypeConstructor
from ._Input import Input


class UFDLJobContract(ABC):
    """
    TODO
    """
    _params: JobContractParams
    _inputs_constructors: Dict[str, Input[Union[TypeConstructor, UFDLType]]]
    _outputs_constructors: Dict[str, Output[Union[TypeConstructor, UFDLType]]]

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
            input_constructor._name = input_name

        if not isinstance(output_constructors, dict):
            raise TypeError(f"Outputs to a job-contract should be a dictionary")

        for output_name, output_constructor in output_constructors.items():
            if not isinstance(output_name, str) or not output_name.isidentifier():
                raise ValueError("All output names must be valid identifiers")
            if not isinstance(output_constructor, Output):
                raise ValueError(f"Output '{output_name}' is not an {Output.__name__}")
            output_constructor._name = output_name

        cls._params = params
        cls._inputs_constructors = input_constructors
        cls._outputs_constructors = output_constructors

    @classmethod
    def params(cls):
        return cls._params

    @classmethod
    def input_constructors(cls):
        return cls._inputs_constructors

    @classmethod
    def output_constructors(cls):
        return cls._outputs_constructors

    @classmethod
    def contract_class_name(cls) -> str:
        name = name_type_translate(cls)
        if name is None:
            raise TypeError(f"No name translation for {cls}")
        return name

    @classmethod
    def format(cls):
        return f"{cls.contract_class_name()}{cls._params}"

    def __init__(
            self,
            types: Dict[str, UFDLType]
    ):
        # Make sure all parameters are specified
        for param in self._params:
            if param.name not in types:
                raise ValueError(f"Contract {self.format()} missing type-argument \"{param.name}\"")

        # Make sure only the parameters are specified
        for name in types:
            if name not in self._params:
                raise ValueError(f"Contract {self.format()} given unknown type-argument \"{name}\"")

        # Attempting to fix all bounds will check for type correctness
        self.params().get_new_bounds_for_fixed(**{
            str(name): type
            for name, type in types.items()
        })

        inputs: Dict[str, Input[UFDLType]] = {
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

        outputs: Dict[str, Output[UFDLType]] = {
            output_name: Output(
                (
                    output_constructor.type.construct(types) if isinstance(output_constructor.type, TypeConstructor)
                    else output_constructor.type
                ),
                help=output_constructor.help
            )
            for output_name, output_constructor in self._outputs_constructors.items()
        }

        for input_name, input in inputs.items():
            input._name = input_name
        for output_name, output in outputs.items():
            output._name = output_name

        self._inputs = inputs
        self._outputs = outputs
        self._types = types

    @property
    def inputs(self):
        return self._inputs

    @property
    def outputs(self):
        return self._outputs

    @property
    def types(self):
        return self._types

    def format_type_args(self) -> str:
        args = tuple(
            self._types[param.name]
            for param in self._params
        )

        if len(args) == 0:
            return ""

        return f"<{', '.join(str(arg) for arg in args)}>"

    def is_subtype_of(self, other: 'UFDLJobContract') -> bool:
        """
        Checks if this contract can be used in place of another contract.

        :param other:
                    The other contract to compare this one to.
        :return:
                    Whether this contract can be used in place of other.
        """
        return (
                type(self) is type(other)
                and all(
                    other_type.is_subtype_of(self_type)
                    for input_name in self.inputs.keys()
                    for self_type, other_type in zip(self.inputs[input_name].types, other.inputs[input_name].types)
                )
                and all(
                    self.outputs[output_name].type.is_subtype_of(other.outputs[output_name].type)
                    for output_name in self.outputs.keys()
                )
        )

    def __str__(self):
        return f"{self.contract_class_name()}{self.format_type_args()}"
